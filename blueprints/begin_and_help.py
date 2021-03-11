from vkwave.bots import (
	DefaultRouter,
	simple_bot_message_handler,
	SimpleBotEvent,
	TextFilter,
	CommandsFilter
)
from vkwave.bots.utils.keyboards import Keyboard

begin_and_help_router = DefaultRouter()

#BEGIN
@simple_bot_message_handler(begin_and_help_router, TextFilter("начать"))
async def begin(event: SimpleBotEvent) -> str:
	kb = Keyboard(one_time=True,inline=False)
	kb.add_text_button("/help")
	kb.add_row()
	kb.add_link_button(text="расписание на сайте",link="http://rasp.pskgu.ru")
	await event.answer(message="выберите действие", keyboard=kb.get_keyboard())

#HELP
@simple_bot_message_handler(begin_and_help_router, CommandsFilter(commands=("help", "справка"), prefixes=("/")))
async def help(event: SimpleBotEvent) -> str:
	m="общий вид команды:"
	m=m+"\n/показать(или /show)  имя (группа или человек)  неделя (по умолчанию стоит текущая, +1 -> след., а -1 -> пред.)"
	m=m+"\nпример команды:"
	m=m+"\n/показать 0431-06 +1"
	m=m+"\n(даная команда покажет следующую неделю группы 0431-06)"
	await event.answer(message=m)