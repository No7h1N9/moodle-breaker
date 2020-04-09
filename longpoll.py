# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from settings import Config


def main(config):
    vk_session = vk_api.VkApi(token=config.ACCESS_TOKEN)
    longpoll = VkBotLongPoll(vk_session, config.GROUP_ID)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            print('Для меня от: ', end='')
            print(event.obj.from_id)
            print('Текст:', event.obj.text)
            print()
        else:
            print(event.type)
            print()


if __name__ == '__main__':
    main(Config())
