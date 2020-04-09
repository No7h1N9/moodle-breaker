import vk


class VkApi:
    def __init__(self, access_token):
        self.session = vk.Session()
        self.api = vk.API(self.session)
        self.access_token = access_token

    def send_message(self, user_id: str, message: str, attachment=""):
        self.api.messages.send(
            access_token=self.access_token, user_id=str(user_id),
            message=message, attachment=attachment)
