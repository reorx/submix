import sys
import argparse
import requests

from .parser import parse_raw_config


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
    else:
        print('Error: please specify a file or url')
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
