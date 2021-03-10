from vkwave.bots import (
	DefaultRouter,
	simple_bot_message_handler,
	SimpleBotEvent,
	CommandsFilter,
)

help_router = DefaultRouter()

@simple_bot_message_handler(help_router, CommandsFilter(commands=("help", "справка"), prefixes=("/")))
async def help(event: SimpleBotEvent) -> str:
	mess="общий вид команды:\n/показать(или /show)  имя (группа или человек)  неделя (по умолчанию стоит текущая, +1 -> след., а -1 -> пред.)\n\nпример команды: \n/показать 0431-06 +1\n(даная команда покажет следующую неделю группы 0431-06)"
	await event.answer(message=mess)