
import rasp.parser

import os.path
import lxml.html

def test_parser():
    root = rasp.parser.request_remote()
    body = root.find("body")
    print(rasp.parser.parse_anchors(body))
