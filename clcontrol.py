
import errors

clients = []

def append(client):
    clients.append(client)


def get_all():
    return clients

def close_all(tasks):
    for cl in clients:
        tasks.append(cl.close())
