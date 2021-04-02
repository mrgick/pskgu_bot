from vkwave.bots import (
	DefaultRouter,
	simple_bot_message_handler,
	SimpleBotEvent,
	TextFilter,
	CommandsFilter,
	PayloadFilter
)
from vkwave.bots.utils.keyboards import Keyboard

begin_and_help_router = DefaultRouter()

#BEGIN, 
@simple_bot_message_handler(begin_and_help_router, TextFilter("начать")|TextFilter("start")|PayloadFilter({"command": "start"}))
async def begin(event: SimpleBotEvent) -> str:
	kb = Keyboard(one_time=True,inline=False)
	kb.add_text_button("/help")
	kb.add_row()
	kb.add_link_button(text="расписание на сайте",link="http://rasp.pskgu.ru")
	await event.answer(message="выберите действие", keyboard=kb.get_keyboard())

#HELP
@simple_bot_message_handler(begin_and_help_router, CommandsFilter(commands=("help", "справка"), prefixes=("/")))
async def help(event: SimpleBotEvent) -> str:
	m="общий вид команд:"
	m=m+"\n/показать(или /show)  имя (группа или человек)  неделя (по умолчанию стоит текущая, +1 -> след., а -1 -> пред.)"
	m=m+"\n/поиск(или find) имя"
	m=m+"\n/подписаться(или subscribe) имя"
	m=m+"\n/отписаться(или unsubscribe)"
	m=m+"\n"
	m=m+"\nпример команд:"
	m=m+"\n/показать 0431-06 +1 - покажет следующую неделю группы 0431-06"
	m=m+"\n/поиск 0431 - поиск по имени 0431"
	m=m+"\n/подписаться 0431-06 - вы подпишитесь на группу 0431-06 и будете получать уведомления"
	m=m+"\n/отписаться - вы отпишитесь от уведомлений"
	await event.answer(message=m)