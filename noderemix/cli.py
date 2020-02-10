import argparse
import requests
import base64
import json
from urllib.parse import urlparse


def main():
    # the `formatter_class` can make description & epilog show multiline
    parser = argparse.ArgumentParser(description="", epilog="", formatter_class=argparse.RawDescriptionHelpFormatter)

    # arguments
    parser.add_argument('file', metavar="FILE", nargs="?", type=str, help="file of downloaded config")

    # options
    #parser.add_argument('-a', '--aa', type=int, default=0, help="")
    #parser.add_argument('-c', '--cc', action='store_true', help="")
    parser.add_argument('-u', '--url', type=str, help="url to download config")
    parser.add_argument('-o', '--output', type=str, help="download url to file, use with -u")

    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r') as f:
            file_content = f.read()
        parse_raw_config(file_content)
    elif args.url:
        resp = requests.get(args.url)
        if args.output:
            with open(args.output, 'wb') as f:
                f.write(resp.content)
        parse_raw_config(resp.content)


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


if __name__ == '__main__':
    main()
