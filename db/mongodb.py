
import motor.motor_asyncio
import pymongo.errors
import errors
import data_types
import components


"""
Обёртка MongoDB
"""
class MongoDB(components.DBComponent):

    def __init__(self, url, name):

        self.name = name
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(url)
            self.db = self.client[name]

            self.url = url # Ни в коем случае не выводить это!

            self.name = name

            self.creation_ex = None
        except pymongo.errors.PyMongoError as ex:
            raise errors.CreationError(ex)

    def __str__(self):
        return "MongoDB '%s'" % self.name

    async def fetch(self, fetch_method, key=None):
        return await getattr(self, "fetch_" + fetch_method)(key)

    async def apply(self, apply_method, applicable):
        return await getattr(self, "apply_" + apply_method)(applicable)

    async def close(self):
        pass

    async def status(self):
        try:
            info = await self.db.command("buildinfo")
            raise errors.StatusSuccess("%s version %s" % (self, info["version"]))
        except pymongo.errors.PyMongoError as ex:
            raise errors.StatusError("%s: %s" % (self, ex))



    async def fetch_search_teacher(self, key):
        pass

    async def fetch_search_group(self, key):
        pass

    async def fetch_group_schedule(self, key):
        pass

    async def fetch_teacher_schedule(self, key):
        pass

    async def fetch_user(self, key):
        pass

    async def apply_group_schedule(self, schedule):
        pass

    async def apply_teacher_schedule(self, schedule):
        pass

    async def apply_user(self, user):
        pass


    
    
