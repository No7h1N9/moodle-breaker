from vk_api.keyboard import VkKeyboardColor, VkKeyboard


class ButtonBase:
    """
    Кнопочка-команда в диалоге
    """
    button_text = ''    # type: str
    button_color = VkKeyboardColor.DEFAULT      # type: str

    def on_click(self, user_id, payload=None):
        pass


class EnterLoginButton(ButtonBase):
    button_text = 'Ввести логин мудла'


class EnterPasswordButton(ButtonBase):
    button_text = 'Ввести пароль мудла'


class BreakProblemButton(ButtonBase):
    button_text = 'Брейкнуть задание'
    button_color = VkKeyboardColor.POSITIVE


class ReportButton(ButtonBase):
    button_text = 'Нашел ошибку'
    button_color = VkKeyboardColor.NEGATIVE


class HelpButton(ButtonBase):
    button_text = 'Помощь'
    button_color = VkKeyboardColor.PRIMARY


class StartAgainButton(ButtonBase):
    button_text = 'В начало'
    button_color = VkKeyboardColor.NEGATIVE


START_BUTTONS = ((BreakProblemButton,),
                 (EnterLoginButton, EnterPasswordButton),
                 (HelpButton, ReportButton))


def build_keyboard(button_groups: iter):
    keyboard = VkKeyboard(one_time=True)
    for button in button_groups[0]:
        keyboard.add_button(button.button_text, button.button_color)
    for row in button_groups[1:]:
        keyboard.add_line()
        for button in row:
            keyboard.add_button(button.button_text, button.button_color)
    return keyboard
