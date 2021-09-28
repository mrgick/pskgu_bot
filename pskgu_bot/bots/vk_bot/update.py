"""
    Отсылает уведомления об обновлениях вк пользователям.
"""

from .bot import vk_send_message
from pskgu_bot.utils import logger
from pskgu_bot.db.services import get_users_by_group, find_group_by_name


async def send_updates_to_users(upd_groups):
    """
        Отсылает уведобмление пользователю об изменении группы.
    """
    logger.info("Start sending messages")
    for group_name in upd_groups:
        users = await get_users_by_group(group_name)
        if users == []:
            continue
        try:
            group = await find_group_by_name(group_name)
            information = group.updated_information
            logger.info("Sending to group="+group_name)
            if information != "":
                for vk_id in users:
                    await vk_send_message(user_id=vk_id,
                                          message=information)
                    # logger.info("Sended message vk_id="+vk_id)
        except Exception as e:
            logger.error(e)
    logger.info(upd_groups)
