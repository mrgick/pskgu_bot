"""
    Файл содержит вк клавиатуры.
"""
import json
from vkwave.bots.utils.keyboards import Keyboard

START_MENU = json.dumps({
    "buttons":
    [[{
        "action": {
            "type": "text",
            "payload": "",
            "label": "/help"
        },
        "color": "primary"
    }],
     [{
         "action": {
             "type": "open_link",
             "label":
             "расписание на сайте",
             "link": "http://rasp.pskgu.ru",
             "payload": ""
         }
     }]],
    "inline":
    False,
    "one_time":
    True
})


def get_start_menu():
    """
        Пример создания клавиатуры.
    """
    start_menu = Keyboard(one_time=True, inline=False)
    start_menu.add_text_button("/help")
    start_menu.add_row()
    start_menu.add_link_button(text="расписание на сайте",
                               link="http://rasp.pskgu.ru")
    return start_menu.get_keyboard()
