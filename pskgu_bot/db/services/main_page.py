"""
    Файл с функциями взаимодействий с классом Main_Page.
"""

from pskgu_bot.db.models import Main_Page, Key
from pskgu_bot.db import local_storage
from pskgu_bot.utils import get_today


async def get_main_page(name):
    main_page = await Main_Page.find_one(filter={'name': name})
    if not main_page:
        main_page = Main_Page(name=name)
        await main_page.commit()
    return main_page


async def get_main_page_hash():
    """
        Получение хеша главной страницы.
    """
    main_page = await get_main_page(name='main_hash')
    return main_page.page_hash


async def set_main_page_hash(page_hash):
    """
        Установление хеша главной страницы.
    """
    main_page = await get_main_page(name='main_hash')
    main_page.page_hash = page_hash
    main_page.information = {get_today(full=True): []}
    await main_page.commit()


async def update_info_main_page():
    """
        Обновление информации об изменении групп.
    """
    def set_dict(info, max_items=20):
        """
            Уменьшает словарь, если он превышает длину.
        """
        while len(info) > max_items:
            info.pop(list(info)[-1])

    main_page = await get_main_page(name='main_info')
    info = dict(main_page.information).copy()
    set_dict(info)
    upd_groups = await local_storage.get(Key("updated_groups"))
    info.update({get_today(full=True): upd_groups})
    main_page.information = info
    await main_page.commit()
    return upd_groups


async def set_main_page_structure(structure):
    """
        Установление структуры расписания.
    """
    main_page = await get_main_page(name='main_info')
    main_page.structure = structure
    await main_page.commit()
