"""
    Файл с моделями.
"""

from .db import instance
from umongo import Document, fields
import typing

Key = typing.NewType("Key", str)


@instance.register
class Group(Document):
    """
        Модель группы, преподавателя.
    """
    name = fields.StringField(required=True, unique=True)
    days = fields.DictField(default={})
    page_url = fields.StringField(default="")
    page_hash = fields.StringField(default="")
    prefix = fields.ListField(fields.StringField())
    last_updated = fields.StringField(default="")
    updated_items = fields.ListField(fields.StringField())
    updated_days = fields.DictField(default={})
    updated_information = fields.StringField(default="")

    class Meta:
        collection_name = "groups"


@instance.register
class Main_Page(Document):
    """
        Модель главной страницы.
    """
    page_hash = fields.StringField(default="")
    information = fields.DictField(default={})
    structure = fields.DictField(default={})

    class Meta:
        collection_name = "pages"


@instance.register
class Vk_User(Document):
    """
        Модель пользователя Вконтакте.
    """
    vk_id = fields.IntegerField(required=True, unique=True)
    group = fields.StringField(default="")

    class Meta:
        collection_name = "vk_users"
