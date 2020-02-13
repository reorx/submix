"""
Considering that "base64 sheme" is the defacto format of subscription config,
it will be the only supported format in the foreseeable future,
so this module is the parser for "base64 scheme subscription config"
"""

import json
import base64
from typing import List
from urllib.parse import urlparse, ParseResult


class Node:
    raw: str
    parsed: ParseResult
    scheme: str
    data_str: str
    data: dict
    name: str

    def __init__(self, raw):
        self.raw = raw
        self.parsed = urlparse(self.raw)
        self.scheme = self.parsed.scheme
        self.data_str = base64.b64decode(self.parsed.netloc.encode()).decode()
        self.data = json.loads(self.data_str)
        if self.scheme == 'vmess':
            self.name = self.data['ps']
        else:
            self.name = ''
        #print(self.data)


NodeList = List[Node]


def parse_raw_sub(raw: bytes) -> NodeList:
    nodes = []
    decoded = base64.b64decode(raw).decode()
    #print(decoded)
    for line in decoded.split('\n'):
        if not line:
            continue
        node = Node(line)
        print(f'{node.name}:\n  {node.raw}')
        nodes.append(node)
    return nodes
