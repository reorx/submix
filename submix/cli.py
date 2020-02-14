import sys
import argparse

import requests

from submix.server import run
from submix.utils import setup_django
from .parser import parse_raw_sub, NodeList


def main():
    # the `formatter_class` can make description & epilog show multiline
    parser = argparse.ArgumentParser(description="", epilog="", formatter_class=argparse.RawDescriptionHelpFormatter)

    # arguments
    parser.add_argument('file', metavar="FILE", nargs="?", type=str, help="file of downloaded subscription")

    # options
    # parser.add_argument('-a', '--aa', type=int, default=0, help="")
    parser.add_argument('-u', '--url', type=str, help="url to download subscription")
    parser.add_argument('-o', '--output', type=str, help="download url to file, use with -u")

    parser.add_argument('-s', '--server', action='store_true', help="start HTTP server")

    args = parser.parse_args()

    nodes: NodeList
    sub_content: bytes
    sub_source: str

    # setup django before running the actual code
    setup_django()

    if args.file:
        sub_source = args.file
        with open(args.file, 'rb') as f:
            sub_content = f.read()
        nodes = parse_raw_sub(sub_content)
    elif args.url:
        sub_source = args.url
        resp = requests.get(args.url)
        sub_content = resp.content
        if args.output:
            with open(args.output, 'wb') as f:
                f.write(sub_content)
        nodes = parse_raw_sub(sub_content)
    else:
        print('Error: please specify a file or url')
        parser.print_help()
        sys.exit(1)

    if args.server:
        run(sub_source, sub_content, nodes)


if __name__ == '__main__':
    main()
