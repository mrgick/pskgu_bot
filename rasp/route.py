# Предназначен для собственной маршрутизации.

import rasp.config
import rasp.utils

import asyncio
import os.path
import urllib.parse
import lxml.html


# Делает нормальный URL.
def normalize_url(url):
    return url.replace("\\", "/")

# Форматирует заголовок (возможно, в будущем, будет
# использоваться для перевода.
def format_title(name):
    return name

# Соединить два путя.
def path_join(path1, path2):
    return (path1 + " -> " if path1 else "") + path2

# Проверяет url на действительность.
def is_valid_url(url):
    return url.rfind("#") == -1

# Узел маршрута.
class Route:

    def __init__(self, parent, hashstr, url, title=None): 
        url = normalize_url(url)
        # Если url неправильный, сделать узел недействительным.
        if not is_valid_url(url):
            self.valid = False
            return

        self.valid = True
        self.parent = parent # Родительский узел
        self.url_dir = url # URL-директория
        self.url = url # URL
        self.children = [] # Дочерние узлы
        self.route_dict = {} # Словарь маршрутов 

        if parent: # Наследование от родительского узла.
            self.route_dict = parent.route_dict # Наследуем словарь маршрутов
            url = os.path.join(parent.url_dir, url) # Наследуем url.
            self.url = url
            # Извлекаем из url url_dir
            ext = os.path.splitext(url)
            if ext[1]:
                self.url_dir = os.path.dirname(url)
            else:
                self.url_dir = url

            # Добавляем узел в родительский.
            parent.children.append(self)

    # Встраиваем маршрут в словарь.
    async def join(self, name):
        async with asyncio.Lock():
            self.route_dict[name] = self 

    # Получить маршрут из словаря.
    def get(self, name):
        return self.route_dict[name]

    def search_by_title(self, query, minmatch):
        result = []
        for route in self.children:
            title = route.title
            if title and rasp.utils.test_by_words(query, title, minmatch=minmatch):
                result.append(route)
        return result
    
    # Получить путь (для вывода пользователю)
    def get_path(self):
        path = ""
        route = self
        while route:
            path = path_join(format_title(route.title), path) 
            route = self.parent
        return path
    
