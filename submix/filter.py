import re


def match(pattern, s):
    return re.search(pattern, s)


# simple filter on name
def filter_nodes_by_name(nodes, include=None, exclude=None):
    l = []
    for n in nodes:
        # TODO checkout schema-cli to improve the code
        if exclude is not None and match(exclude, n.name):
            continue
        if include is not None and match(include, n.name):
            l.append(n)
    return l
