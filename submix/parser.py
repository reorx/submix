"""
Considering that "base64 sheme" is the defacto format of subscription config,
it will be the only supported format in the foreseeable future,
so this module is the parser for "base64 scheme subscription config"
"""

from typing import List
from dataclasses import dataclass, field

import json
import base64
from urllib.parse import urlparse, ParseResult
from .utils import base64_encode_str


@dataclass
class Node:
    name: str
    protocol: str
    data: dict
    _data_str: str = field(init=False, repr=False)
    _url: str = field(init=False, repr=False)
    _url_parsed: ParseResult = field(init=False, repr=False)

    def get_url(self) -> str:
        if self._url:
            return self._url
        netloc = base64_encode_str(json.dumps(self.data))
        return f'{self.protocol}://{netloc}'

    @classmethod
    def new_from_url(cls, url):
        url_parsed = urlparse(url)
        protocol = url_parsed.scheme
        data_str = base64.b64decode(url_parsed.netloc.encode()).decode()
        data = json.loads(data_str)
        name = ''
        if protocol == 'vmess':
            name = data['ps']

        node = cls(
            protocol=protocol,
            data=data,
            name=name,
        )

        # set private attrs
        node._url = url
        node._url_parsed = url_parsed
        node._data_str = data_str

        # print(node.data)
        return node


NodeList = List[Node]


def parse_raw_sub(raw: bytes) -> NodeList:
    nodes = []
    decoded = base64.b64decode(raw).decode()
    # print(decoded)
    for line in decoded.split('\n'):
        if not line:
            continue
        node = Node.new_from_url(line)
        print(f'{node.name}:\n  {node.get_url()}')
        nodes.append(node)
    return nodes
