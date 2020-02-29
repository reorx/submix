"""
Considering that "base64 sheme" is the defacto format of subscription config,
it will be the only supported format in the foreseeable future,
so this module is the parser for "base64 scheme subscription config"

url: https://github.com/2dust/v2rayN/wiki/%E8%AE%A2%E9%98%85%E5%8A%9F%E8%83%BD%E8%AF%B4%E6%98%8E
"""
from io import StringIO
from typing import List
from dataclasses import dataclass, field

import json
import base64
from urllib.parse import urlparse, ParseResult, unquote
from .utils import base64_encode_str, base64_decode_str, get_base64_config_from_url
from .log import base_lg
from .protocols import Protocol, VmessConfig


lg = base_lg.getChild(__name__)


@dataclass(init=False)
class Node:
    protocol: str
    name: str
    ip: str
    port: int
    hash: str
    config: dict

    _url: str = field(repr=False)
    _url_parsed: ParseResult = field(repr=False)

    @property
    def url(self) -> str:
        if self._url:
            return self._url
        netloc = base64_encode_str(json.dumps(self.config))
        return f'{self.protocol}://{netloc}'

    def get_vmess(self) -> VmessConfig:
        Protocol.check(self.protocol, Protocol.vmess)
        return VmessConfig.from_dict(self.config)

    @classmethod
    def new_from_url(cls, url) -> 'Node':
        unquoted_url = unquote(url)
        lg.debug(f'url (unquoted): {unquoted_url}')
        n = cls()
        url_parsed = urlparse(unquoted_url)
        lg.debug(f'url_parsed: {url_parsed}')
        n.protocol = url_parsed.scheme
        if n.protocol == Protocol.vmess:
            # because base64 may contain `/`, it's not suitable to use url_parsed.netloc
            # to get the base64 content, therefore we use this special helper function
            n.config = get_base64_config_from_url(url, n.protocol)
            vmess = n.get_vmess()
            n.name = vmess.ps
            n.ip = vmess.add
            n.port = vmess.port
        elif n.protocol == Protocol.ssr:
            n.config = get_base64_config_from_url(url, n.protocol)
        elif n.protocol == Protocol.ss:
            n.config = {}
            n.name = url_parsed.fragment
        else:
            raise ValueError('Cannot recognize protocol {n.protocol} in url')

        # set private attrs
        n._url = url
        n._url_parsed = url_parsed

        lg.debug(f'config: {n.config}')
        return n


NodeList = List[Node]


def parse_raw_sub(raw: bytes) -> NodeList:
    nodes = []
    f = StringIO(base64.b64decode(raw).decode())
    for line in f.readlines():
        line = line.strip()
        lg.debug(f'line: {line}')
        if not line:
            continue
        node = Node.new_from_url(line)
        lg.debug(f'node: name={node.name}\n  url={node.url}')
        nodes.append(node)
    return nodes
