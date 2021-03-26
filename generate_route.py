#!generate_route.py
# Автоматически генерирует маршрут.

import rasp.route
import rasp.parser

import os.path
import lxml.html
import re

root = None

def generate_by_regex(regex, parent, anchor):
    content = ''.join(anchor.itertext())
    for item in regex:
        m = re.match(item[0], content)
        if m:
            route = rasp.route.Route(parent, item[1], anchor.get("href"), item[2])
            item[3](route, anchor, m.group(1))
            route.join()

def generate_inst(route, anchor, title):
    print(route.parent)
    route.rename(os.path.basename(route.url_dir))
    print(route.url_dir)
    route.title = title

ROUTE_INST_REGEX = [
    [r"(.*)", None, None, generate_inst]
]
def generate_fulltime(route, anchor, title):
    for anchor in rasp.parser.parse_anchors(rasp.route.request_remote(route.url).find("body")):
        generate_by_regex(ROUTE_INST_REGEX, route, anchor) 

def generate_ext(route, anchor, title):
    print(title)

def generate_teachers(route, anchor, title):
    print(title)

ROUTE_ROOT_REGEX = [
    [r"(.*ОФО.*)", "ft", "", generate_fulltime],
    [r"(.*ЗФО.*)", "ext", "Заочная форма обучения (ЗФО)", generate_ext],
    [r"(.*преподавателей.*)", "teachers", "Преподаватели", generate_teachers],
]
def generate_root(root):
    for anchor in rasp.parser.parse_anchors(rasp.route.request_remote().find("body")):
        generate_by_regex(ROUTE_ROOT_REGEX, root, anchor)

def generate_route():
    global root 
    root = rasp.route.Route(None, None, "") 
    generate_root(root)

def go_to_path(path):
    return root.go(path)

def get_root():
    return root
