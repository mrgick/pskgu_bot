
class BaseComponent():
    def __init__(self):
        pass

    def __str__(self):
        pass

    async def status(self):
        pass

    async def close(self):
        pass

class DBComponent(BaseComponent):

    async def fetch(self, fetch_method, dbkey):
        pass

    async def apply(self, apply_method, applicable):
        pass

class ClComponent(BaseComponent):

    async def notify(self, user, notify_method, notifiable):
        pass
