from vkbottle import (Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD)

show_keyboard = Keyboard(one_time=False, inline=False)
show_keyboard.add(Text("/show"), color=KeyboardButtonColor.PRIMARY)
show_keyboard.row()
show_keyboard.add(Text("/show 1"), color=KeyboardButtonColor.PRIMARY)
SHOW_BUTTONS_KEYBOARD = show_keyboard.get_json()
