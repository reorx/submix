"""
Considering that "base64 sheme" is the defacto format of subscription config,
it will be the only supported format in the foreseeable future,
so this module is the parser for "base64 scheme subscription config"
"""

import json
import base64
from urllib.parse import urlparse


class ProxyURL:
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


def parse_raw_config(raw: bytes):
    cfg_str = base64.b64decode(raw).decode()
    #print(cfg_str)
    for line in cfg_str.split('\n'):
        if not line:
            continue
        url = ProxyURL(line)
        print(f'{url.name}:\n  {url.raw}')
    return cfg_str
