"""
    Файл с моделями для парсера
"""

from pskgu_bot import Config
import os.path


class Anchor:
    """
        Класс Якорь (пошло от html тега <a>).
        Хранит в себе ссылку и имя страницы.
    """
    __slots__ = ('href', 'title')

    def __init__(self, href, title):
        self.href = str(href)
        self.title = str(title)


class Route:
    """
        Узел маршрута.
    """

    __slots__ = ('valid', '_url', 'prefix')

    def __init__(self, url, parent=None, prefix=None):
        """
            Инициализация класса.
        """
        self.valid = self.check_valid(url)
        if not self.valid:
            return

        url = self.normolize_url(url)
        self._url = url

        self.prefix = []
        if parent:
            if parent.prefix:
                self.prefix.extend(parent.prefix)
        if prefix:
            self.prefix.append(prefix)

    @property
    def url(self):
        return Config.REMOTE_URL + "/" + self._url

    def normolize_url(self, url):
        """
            Делает нормальный URL.
        """
        return url.replace("\\", "/")

    def check_valid(self, url):
        """
            Проверяет url на действительность.
        """
        return (url.rfind("#") == -1 and url.rfind("\\0.html") == -1)
