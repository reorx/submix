from dataclasses import dataclass


class Protocol:
    vmess = 'vmess'
    ssr = 'ssr'
    ss = 'ss'
    # ssd = 'ssd'

    @classmethod
    def check(cls, protocol, value):
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
    def from_dict(cls, d: dict) -> 'VmessConfig':
        c = VmessConfig()
        for k, v in d.items():
            setattr(c, k, v)
        return c


# SSD
# ref: https://github.com/TheCGDF/SSD-Windows/wiki/HTTP%E8%AE%A2%E9%98%85%E5%8D%8F%E5%AE%9A
