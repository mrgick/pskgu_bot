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
    __slots__ = ('href', 'title', 'course')

    def __init__(self, href, title, course=None):
        self.href = str(href)
        self.title = str(title)
        self.course = course


class Route:
    """
        Узел маршрута.
    """

    __slots__ = ('valid', '_url', 'prefix')

    def __init__(self, url, parent=None, prefix=None, course=None):
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
                if course:
                    self.prefix.append(str(course))
        if prefix:
            self.prefix.append(prefix)

    @property
    def url(self):
        if (len(self.prefix) > 0 and self.prefix[0] == 'колледж'
                and not self._url.endswith('/k')):
            return Config.REMOTE_URL + "/k/" + self._url
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
