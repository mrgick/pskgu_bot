#!rasp_parser.py
# Предназначен для парсинга расписания,
# а также для поиска пути.

import rasp.config

import urllib.request
import lxml.html
import os.path

# Парсит якори.
def parse_anchors(html_element):
    return list(filter((lambda x: x.tag == "a"), html_element))
        
