#!rasp/route.py
# Предназначен для собственной маршрутизации,
# чтобы было легче поддерживать это говно.

import os.path

def normalize_url(url):
    return url.replace("\\", "/")

def format_name(name):
    return name

def test_query(query, name):
    return bool(re.match(r"\B" + re.escape(query) + r"\B", name))

def split_path(path):
    return path.split("->", maxsplit=1)

# Отправляет запрос на удалённый хост с расписанием. Возвращает DOM.
def request_remote(url=""):
    full_url = os.path.join(rasp.config.REMOTE_URL, url)
    return lxml.html.parse(full_url)



class RouteError(RuntimeError):
    def __init__(self, r, full_path):
        self.msg = "%s (%s): Invalid path!" % (full_path, r.url) 

# Узел маршрута.
class Route:

    def __init__(self, parent, tag, name, url): 
        self.parent = parent
        self.name = name
        self.url_dir = url
        self.url = url
        self.title = title 
        self.children = []
        self.tag_dict = {}
        self.tag = tag

    def join(self):
        parent = self.parent
        url = normalize_url(self.url)
        if parent:
            self.tag_dict = parent.tag_dict
            self.tag = os.path.join(parent.tag, self.tag)
            url = os.path.join(parent.url_dir, url)
            self.url = url
            ext = os.path.splitext(url)
            if ext[1]:
                self.url_dir = os.path.dirname(url)
            else:
                self.url_dir = url
            if name:
                parent.children.push(self)
        if self.tag:
            self.tag_dict[self.tag] = self 
    
    # Пойти по маршруту.
    def go(self, path, full_path=""):
        route = self
        path = normalize_url(path)
        while True:
            pair = path.split("/", maxsplit=1)
            route_dict = self.children_dict
                
            full_path = os.path.join(full_path, pair[0])
            if pair[0] not in route_dict:
                raise RouteError(self, full_path)
            if len(pair) == 1:
                return route_dict[pair[0]]
            route = route_dict[pair[0]]
            path = pair[1]
    
    def get_path(self):
        path = ""
        route = self
        while route:
            path = format_name(route.name) + (" -> " + path if path else "")
            route = self.parent
        return path
    
    def search(self, path):
        pass
