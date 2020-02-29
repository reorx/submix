import logging
import sys
import argparse

import requests

from submix.filter import filter_nodes_by_name
from submix.server import run
from submix.utils import setup_django
from .parser import parse_raw_sub, NodeList
from .log import base_lg
from . import settings


def main():
    # the `formatter_class` can make description & epilog show multiline
    parser = argparse.ArgumentParser(description="", epilog="", formatter_class=argparse.RawDescriptionHelpFormatter)

    # arguments
    parser.add_argument('file', metavar="FILE", nargs="?", type=str, help="file of downloaded subscription")

    # options
    # parser.add_argument('-a', '--aa', type=int, default=0, help="")
    parser.add_argument('-u', '--url', type=str, help="url to download subscription")
    parser.add_argument('-o', '--output', type=str, help="download url to file, use with -u")

    # filter
    parser.add_argument('-i', '--include', type=str, help="")
    parser.add_argument('-e', '--exclude', type=str, help="")
    parser.add_argument('--human', action='store_true', help="print human readable")

    parser.add_argument('-s', '--server', action='store_true', help="start HTTP server")
    parser.add_argument(
        '-d', '--debug', action='count', default=0,
        help="""\
-d: set submix logger level to DEBUG;
-dd: set all loggers (in settings.LOGGING) level to DEBUG;
-ddd: set all loggers and root logger level to DEBUG.""")

    args = parser.parse_args()

    nodes: NodeList
    sub_content: bytes
    sub_source: str

    # setup django before running the actual code
    setup_django()

    if args.debug >= 1:
        base_lg.setLevel(logging.DEBUG)
    if args.debug >= 2:
        for logger_name in settings.LOGGING['loggers']:
            logging.getLogger(logger_name).setLevel(logging.DEBUG)
    if args.debug >= 3:
        logging.getLogger().setLevel(logging.DEBUG)
    base_lg.debug('DEBUG level enabled')

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

    # filter and print
    filtered_nodes = filter_nodes_by_name(nodes, args.include, args.exclude)
    for n in filtered_nodes:
        if args.human:
            print(f'{n.name}\n{n.url}')
        else:
            print(n.url)

    if args.server:
        run(sub_source, sub_content, nodes)


if __name__ == '__main__':
    main()
