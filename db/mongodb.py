
import motor.motor_asyncio
import pymongo.errors
import data_types


"""
Обёртка MongoDB
"""
class MongoDB:

    def __init__(self, url, name):

        self.name = name
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(url)
            self.db = self.client[name]

            self.url = url # Ни в коем случае не выводить это!

            self.name = name

            self.creation_ex = None
        except pymongo.errors.PyMongoError as ex:
            self.creation_ex = ex

    def __str__(self):
        return "MongoDB '%s'" % self.name

    async def fetch(self, fetch_method, key=None):
        return await getattr(self, "fetch_" + fetch_method)(key)

    async def apply(self, apply_method, applicable):
        return await getattr(self, "apply_" + apply_method)(applicable)

    async def close(self):
        pass

        
    async def fetch_status(self, key):
        if self.creation_ex: 
            return data_types.Status(ex=self.creation_ex)
        try: 
            info = await self.db.command("buildinfo")
            return data_types.Status(
                msg="Version %s" % info["version"])
        except pymongo.errors.PyMongoError as ex:
            return data_types.Status(ex=ex)

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


    
    
