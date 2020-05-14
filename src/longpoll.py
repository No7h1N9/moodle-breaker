# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import os
from typing import List
import sentry_sdk
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from requests.exceptions import ReadTimeout
from utils import logger
from time import sleep

from vk_api.utils import get_random_id

from models import DatabaseManager
from moodle_api.network import MoodleAPI
from moodle_api.breaker import break_task
from moodle_api.parsers import parse_cmid
from messages import *
from commands.buttons import *


manager = DatabaseManager(os.environ.get('DATABASE_URL'))
#sentry_sdk.init(
#    dsn="https://5de487140b7e4a2bb9a408c6dc18d471@o389213.ingest.sentry.io/5227091",
#    integrations=[SqlalchemyIntegration()]
#)
vk_session = vk_api.VkApi(token=os.environ.get('ACCESS_TOKEN'))
longpoll = VkBotLongPoll(vk_session, os.environ.get('GROUP_ID'))
vk = vk_session.get_api()


def send_message(to_id, message: str, keyboard: VkKeyboard = None) -> None:
    vk.messages.send(
        peer_id=to_id,
        random_id=get_random_id(),
        keyboard=getattr(keyboard, 'get_keyboard', lambda: None)(),
        message=message)


def parse_credentials(message_text: str) -> List[str]:
    parsed = message_text.split('\n')
    assert len(parsed) == 2
    return parsed


def valid_credentials(login, password):
    api = MoodleAPI(login, password)
    api.auth()
    return api.is_authorized


def handle_message(event):
    message_text, message_id = event.obj.text, event.obj.id
    user_id = int(event.obj.from_id)
    if manager.first_seen(user_id):
        send_message(user_id, FIRST_ENTRY_MESSAGE)
        manager.add_user(user_id, '', '')
        return
    if manager.get_user(user_id).empty_credentials:
        try:
            login, password = parse_credentials(message_text)
            send_message(user_id, CORRECT_LOGIN_INPUT)
            if valid_credentials(login, password):
                manager.update_user(user_id, login, password)
                send_message(user_id, MOODLE_ACCEPTED_LOGIN)
            else:
                send_message(user_id, MOODLE_DECLINED_LOGIN)
        except AssertionError:
            send_message(user_id, INCORRECT_LOGIN_INPUT)
            return
    else:
        user = manager.get_user(user_id)
        try:
            cmid = parse_cmid(message_text)
        except ValueError:
            send_message(user_id, INCORRECT_TASK_URL)
            return
        send_message(user_id, CORRECT_TASK_URL)
        api = MoodleAPI(login=user.login, password=user.password)
        broken, unbroken = break_task(api, cmid)
        if not unbroken and broken:
            send_message(user_id, BREAKING_DONE)
        else:
            send_message(user_id, FIELDS_ARE_MISSING)


def main():
    for event in longpoll.listen():
        # Пока только проверяем входящие сообщения
        if event.type == VkBotEventType.MESSAGE_NEW:
            handle_message(event)


if __name__ == '__main__':
    while True:
        try:
            main()
        except ReadTimeout as e:
            logger.error(f'lost connection with vk. Retrying in 10 seconds... Error: {e}')
            sleep(10)


