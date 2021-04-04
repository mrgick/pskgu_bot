from vkwave.bots import (
    DefaultRouter,
    simple_bot_message_handler,
    SimpleBotEvent,
    CommandsFilter,
    PhotoUploader
)
from config import bot

map_router = DefaultRouter()

@simple_bot_message_handler(map_router, CommandsFilter(commands=("map", "карта"), prefixes=("/")))
async def help(event: SimpleBotEvent) -> str:
    peer_id=event.object.object.message.peer_id
    big_attachment = await PhotoUploader(bot.api_session.api.get_context()).get_attachments_from_links(
        peer_id=peer_id,
        links=[
            "https://cdn.discordapp.com/attachments/824647324981657620/825467801774718986/SPOILER_1etage.png",
            "https://cdn.discordapp.com/attachments/824647324981657620/825467805477503026/SPOILER_2etage.png",
            "https://cdn.discordapp.com/attachments/824647324981657620/825467806924800040/SPOILER_3etage.png",
            "https://cdn.discordapp.com/attachments/824647324981657620/825467882536042516/SPOILER_4etage.png",
        ],
    )
    await bot.api_session.api.get_context().messages.send(user_id=peer_id, attachment=big_attachment, random_id=0)

