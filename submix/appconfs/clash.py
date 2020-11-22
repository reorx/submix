from typing import Union
import re
import yaml
import argparse


def load_conf(filepath):
    with open(filepath) as f:
        return ClashConf(yaml.load(f.read(), Loader=yaml.FullLoader))


def match_one(pattern, s):
    return re.search(pattern, s)


def match_one_of(patterns, s):
    for i in patterns:
        if match_one(i, s):
            return True
    return False


class EasyFilterList:
    def __init__(self, items, item_type='object'):
        self.items = items
        self.item_type = item_type

    def __iter__(self):
        return iter(self.items)

    def filter(self, key='name', include: Union[str, list, None] = None, exclude: Union[str, list, None] = None):
        l = self.items

        if self.item_type == 'object':
            def get_v(item):
                return getattr(item, key)
        else:
            def get_v(item):
                return item[key]

        if include:
            if isinstance(include, str):
                l = [i for i in l if match_one(include, get_v(i))]
            else:
                l = [i for i in l if match_one_of(include, get_v(i))]

        if exclude:
            if isinstance(exclude, str):
                l = [i for i in l if not match_one(exclude, get_v(i))]
            else:
                l = [i for i in l if not match_one_of(exclude, get_v(i))]

        return EasyFilterList(l, item_type=self.item_type)


# proxy_tpl = """\
# {name} - [{type}] - {cipher}:{password}@{server}:{port}"""
proxy_tpl = """\
{name} [{type}]
    {server} : {port} cipher={cipher} pass={password}"""


class ClashConf:
    def __init__(self, data):
        self.data = data
        self.proxies = EasyFilterList(data['proxies'], item_type='dict')

    def print_proxies(self, proxies):
        for i in proxies:
            print(proxy_tpl.format(**i))


class AppendDict(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not 'ordered_args' in namespace:
            setattr(namespace, 'ordered_args', [])
        previous = namespace.ordered_args
        previous.append({self.dest: values})
        setattr(namespace, 'ordered_args', previous)


def main():
    # the `formatter_class` can make description & epilog show multiline
    parser = argparse.ArgumentParser(description="", epilog="", formatter_class=argparse.RawDescriptionHelpFormatter)

    # arguments
    parser.add_argument('file', metavar="FILE", nargs=1, type=str, help="file of clash config")

    # options
    # parser.add_argument('-a', '--aa', type=int, default=0, help="")
    parser.add_argument('-i', '--include', type=str, action=AppendDict, help="")
    parser.add_argument('-e', '--exclude', type=str, action=AppendDict, help="")

    args = parser.parse_args()
    print('args', args)

    cc = load_conf(args.file[0])

    pxs = cc.proxies
    for kwargs in args.ordered_args:
        pxs = pxs.filter(**kwargs)

    cc.print_proxies(pxs)


if __name__ == "__main__":
    main()
