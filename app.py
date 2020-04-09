from flask import Flask, Blueprint, request, current_app
from vk_api import VkApi
import json

from settings import Config


api = Blueprint('api', __name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.vk_api = VkApi(access_token=app.config['ACCESS_TOKEN'])
    app.register_blueprint(api)
    return app


@api.route('/', methods=['POST'])
def handle_vk_request():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return current_app.config['CONFIRMATION_TOKEN']
    elif data['type'] == 'message_new':
        incoming_message = data['object']
        current_app.vk_api.send_message(incoming_message['user_id'], 'Hello there!')
        return 'ok'
    return 'ok'


if __name__ == '__main__':
    app = create_app()
    app.run()
