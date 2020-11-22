import json
import re
from dataclasses import dataclass
from urllib.parse import urlparse, parse_qs

from .utils import base64_decode_str
from .log import base_lg


lg = base_lg.getChild('protocols')


class Protocol:
    vmess = 'vmess'
    ssr = 'ssr'
    ss = 'ss'
    # ssd = 'ssd'

    @classmethod
    def assert_equal(cls, protocol, value):
        if protocol != value:
            raise ValueError(f'Must use protocol {value}, got {protocol}')


# Vmess
# ref: https://github.com/2dust/v2rayN/wiki/%E5%88%86%E4%BA%AB%E9%93%BE%E6%8E%A5%E6%A0%BC%E5%BC%8F%E8%AF%B4%E6%98%8E(ver-2)
@dataclass(init=False)
class VmessConfig:
    """
    json: {
      "v": "2",
      "ps": "Name of Vmess Server",
      "add": "224.0.0.1",
      "port": 321,
      "id": "dc9380p4-abf3-3769-9809-b02b6e306058",
      "aid": "58",
      "net": "ws",
      "type": "none",
      "host": "foo.bar.com",
      "path": "/",
      "mux": {
        "enabled": "false"
      }
    }
    """
    v: str
    ps: str
    add: str
    port: int
    id: str
    aid: str
    net: str
    type: str
    host: str
    path: str
    mux: dict
    tls: str

    @classmethod
    def from_str(cls, config: str) -> 'VmessConfig':
        lg.debug(f'VmessConfig <- {config}')
        try:
            d = json.loads(config)
        except ValueError:
            print(f'json.loads: {config}')
            raise
        c = VmessConfig()
        for k, v in d.items():
            setattr(c, k, v)
        return c


ssr_regex = re.compile('^([^:]+):([^:]+):([^:]*):([^:]+):([^:]*):([^:]+)$')


# SSR
# ref: https://github.com/shadowsocksrr/shadowsocksr-csharp/blob/master/shadowsocks-csharp/Model/Server.cs
@dataclass(init=False)
class SSRConfig:
    """
    ssr://host:port:protocol:method:obfs:base64pass/?obfsparam=base64&remarks=base64&group=base64&udpport=0&uot=1

    example:
    ssr://224.10.10.10:27815:origin:chacha20:plain:UEBzc3dvcmQK/?remarks=6IqC54K55ZCN56ewCg&group=TXkgR3JvdXAK
    """
    host: str
    port: int
    protocol: str
    method: str
    obfs: str
    base64pass: str
    remarks: str
    group: str
    params: dict

    @classmethod
    def from_str(cls, url: str) -> 'SSRConfig':
        lg.debug(f'SSRConfig <- {url}')
        url_parsed = urlparse(url)
        rv = ssr_regex.search(url_parsed.netloc)
        if not rv:
            raise ValueError(f'cannot match SSRConfig from str: {url_parsed.netloc}')
        g = rv.groups()
        c = SSRConfig()

        # netloc
        c.host = g[0]
        c.port = int(g[1])
        c.protocol = g[2]
        c.method = g[3]
        c.obfs = g[4]
        c.base64pass = g[5]

        # query
        if url_parsed.query:
            q = {k: v[0] for k, v in parse_qs(url_parsed.query).items()}
            c.remarks = base64_decode_str(q.get('remarks', ''))
            c.group = base64_decode_str(q.get('group', ''))
            c.params = q
        else:
            c.remarks = ''
            c.group = ''
            c.params = {}

        return c


# SSD
# ref: https://github.com/TheCGDF/SSD-Windows/wiki/HTTP%E8%AE%A2%E9%98%85%E5%8D%8F%E5%AE%9A
