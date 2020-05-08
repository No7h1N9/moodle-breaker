# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from collections import defaultdict
import sentry_sdk

from vk_api.utils import get_random_id

from commands import handle_free_input
from settings import Config
from commands.buttons import *
from itertools import chain


sentry_sdk.init("https://5de487140b7e4a2bb9a408c6dc18d471@o389213.ingest.sentry.io/5227091")
vk_session = vk_api.VkApi(token=Config().ACCESS_TOKEN)
longpoll = VkBotLongPoll(vk_session, Config().GROUP_ID)
vk = vk_session.get_api()


is_free_input = defaultdict(lambda: False)
user_states = defaultdict(lambda: 0)


def resend_menu(user_id):
    send_message(user_id, 'Некорректный ввод. Попробуй выбрать вариант из кнопки',
                 keyboard=build_keyboard(current_buttons()))


def send_message(to_id, message: str, keyboard: VkKeyboard = None) -> None:
    vk.messages.send(
        peer_id=to_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=message)

def current_buttons():
    return START_BUTTONS


def handle_button(button_text, user_id):
    for button in chain(*current_buttons()):
        if button_text in button.button_text:
            button.on_click(user_id)
            return True
    return False


def main():
    for event in longpoll.listen():
        # Пока только проверяем входящие сообщения
        if event.type == VkBotEventType.MESSAGE_NEW:
            message, user_id = event.obj.text, event.obj.from_id
            if not is_free_input[user_id]:
                if not handle_button(message, user_id):
                    resend_menu(user_id)
            else:
                handle_free_input(user_states[user_id], message)


if __name__ == '__main__':
    setup_db('sqlite://memory')
    main()


