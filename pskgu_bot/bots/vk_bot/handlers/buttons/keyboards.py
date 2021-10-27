from vkbottle import (Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD)


def get_show_shifted_keyboard(week: int = 0):
    keyboard = Keyboard(one_time=False, inline=False)
    keyboard.add(Text("Текущая неделя",
                      payload={
                          "command": "show",
                          "week": 0
                      }),
                 color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Предыдущая",
                      payload={
                          "command": "show",
                          "week": week - 1
                      }),
                 color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("Следующая",
                      payload={
                          "command": "show",
                          "week": week + 1
                      }),
                 color=KeyboardButtonColor.PRIMARY)
    return keyboard.get_json()


def get_show_keyboard():
    keyboard = Keyboard(one_time=False, inline=False)
    keyboard.add(Text("/show"), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("/show 1"), color=KeyboardButtonColor.PRIMARY)
    return keyboard.get_json()
