
import data_types
import vkwave.bots
import errors
import components
from vkwave.api.methods._error import APIError

class VKBot(components.ClComponent):
    def __init__(self, api_token, group_id):
        self.token = api_token
        self.group_id = group_id
        self.name = "vk"

        self.bot = vkwave.bots.SimpleLongPollBot(
            tokens=api_token, group_id=api_token)

    def __str__(self):
        return "VK Bot"

    async def status(self):
        try:
            await self.bot.api_context.utils.get_server_time()
            raise errors.StatusSuccess("%s Long Poll API" % self)
        except APIError as ex:
            raise errors.StatusError("%s: %s" % (self, ex))
            

    async def close(self):
        await self.bot.api_session.close()
