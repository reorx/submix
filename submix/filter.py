import re


def match(pattern, s):
    return re.search(pattern, s)


# simple filter on name
def filter_nodes_by_name(nodes, include=None, exclude=None):
    # TODO improve code from schema-cli
    l = list(nodes)
    if include is not None:
        l = [n for n in l if match(include, n.name)]
    if exclude is not None:
        l = [n for n in l if not match(exclude, n.name)]
    return l
