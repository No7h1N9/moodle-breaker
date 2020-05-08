# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from collections import defaultdict
import sentry_sdk

from vk_api.utils import get_random_id

from settings import Config
from commands.buttons import *


sentry_sdk.init("https://5de487140b7e4a2bb9a408c6dc18d471@o389213.ingest.sentry.io/5227091")
vk_session = vk_api.VkApi(token=Config().ACCESS_TOKEN)
longpoll = VkBotLongPoll(vk_session, Config().GROUP_ID)
vk = vk_session.get_api()


def send_message(to_id, message: str, keyboard: VkKeyboard = None) -> None:
    vk.messages.send(
        peer_id=to_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=message)


def main():
    for event in longpoll.listen():
        # Пока только проверяем входящие сообщения
        if event.type == VkBotEventType.MESSAGE_NEW:
            message, user_id = event.obj.text, event.obj.from_id


if __name__ == '__main__':
    setup_db('sqlite://memory')
    main()


