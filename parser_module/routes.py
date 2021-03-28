# Предназначен для собственной маршрутизации.
import asyncio
import os.path
import lxml.html


# Узел маршрута.
class Route:

    def __init__(self, parent, url, prefix): 
        # Делает нормальный URL.
        url = url.replace("\\", "/")
        # Проверяет url на действительность.
        if not url.rfind("#") == -1:
            self.valid = False
            return

        self.valid = True
        self.parent = parent # Родительский узел
        self.url_dir = url # URL-директория
        self.url = url # URL
        self.prefix = prefix

        if parent: # Наследование от родительского узла.
            url = os.path.join(parent.url_dir, url) # Наследуем url.
            self.url = url
            # Извлекаем из url url_dir
            ext = os.path.splitext(url)
            if ext[1]:
                self.url_dir = os.path.dirname(url)
            else:
                self.url_dir = url
                
            if parent.prefix != "":
                self.prefix = parent.prefix