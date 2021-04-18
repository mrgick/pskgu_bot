
clients = []

async def append(client):
    status = await client.status()
    if not status.ex:
        clients.append(client)

    return status

def get_all():
    return clients

def close_all(tasks):
    for cl in clients:
        tasks.append(cl.close())
