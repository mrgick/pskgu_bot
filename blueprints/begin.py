from vkwave.bots import (
	DefaultRouter,
	simple_bot_message_handler,
	SimpleBotEvent,
	TextFilter,
)
from vkwave.bots.utils.keyboards import Keyboard

begin_router = DefaultRouter()

@simple_bot_message_handler(begin_router, TextFilter("начать"))
async def begin(event: SimpleBotEvent) -> str:
	kb = Keyboard(one_time=True,inline=False)
	kb.add_text_button("/help")
	kb.add_row()
	kb.add_link_button(text="расписание на сайте",link="http://rasp.pskgu.ru")
	await event.answer(message="выберите действие", keyboard=kb.get_keyboard())