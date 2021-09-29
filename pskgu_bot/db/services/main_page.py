"""
    Файл с функциями взаимодействий с классом Main_Page.
"""

from pskgu_bot.db.models import Main_Page, Key
from pskgu_bot.db import local_storage
from pskgu_bot.utils import get_today


async def get_main_page_hash():
    """
        Получение хеша главной страницы.
    """
    main_page = await Main_Page.find_one()
    if not main_page:
        main_page = Main_Page()
        await main_page.commit()
    return main_page.page_hash


async def set_main_page_hash(page_hash):
    """
        Получение хеша главной страницы.
    """
    main_page = await Main_Page.find_one()
    main_page.page_hash = page_hash
    await main_page.commit()


async def update_info_main_page():
    """
        Обновление информации об изменении групп.
    """
    def set_dict(info, max_items=100):
        """
            Возвращает уменьшенный словарь, если он превышает длину.
        """
        new_info = info.copy()
        if len(info) > max_items:
            for key, value in info.items():
                if len(new_info) <= max_items:
                    break
                else:
                    new_info.pop(key)
            info = new_info
        return info

    main_page = await Main_Page.find_one()
    info = set_dict(main_page.information)
    upd_groups = await local_storage.get(Key("updated_groups"))
    info.update({get_today(full=True): upd_groups})
    main_page.information = info
    await main_page.commit()
    return upd_groups
