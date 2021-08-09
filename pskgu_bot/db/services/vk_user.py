"""
    Файл с функциями взаимодействий с бд.
"""

from pskgu_bot.db.models import Vk_User


def is_vk_user_subscribed(user):
    """
        Проверяет подписан ли человек на группу.
    """
    if user:
        return user.group != ""
    return False


async def get_users_by_group(group):
    """
        Возвращает ид пользователей, найденных у данной группы.
    """
    return [x.vk_id async for x in Vk_User.find(filter={"group": group})]


async def find_vk_user_by_id(vk_id):
    """
        Находит пользователя по id.
    """
    return await Vk_User.find_one(filter={"vk_id": int(vk_id)})


async def update_user(vk_id, group):
    """
        Обновляет или создаёт экземпляр класса Vk_User.
    """
    user = await find_vk_user_by_id(vk_id)
    if user:
        user.group = group
    else:
        user = Vk_User(vk_id=int(vk_id), group=group)
    await user.commit()


async def delete_user(vk_id):
    """
        Удаляет вк пользователя из бд.
    """
    user = await find_vk_user_by_id(vk_id)
    if user:
        await user.remove()
