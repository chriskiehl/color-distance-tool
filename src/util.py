"""
A collection of functional utilities/helpers
"""
from copy import deepcopy
from functools import reduce

def fix(f, *args):
    """Apply the supplied function to a fixed arg"""
    return lambda *x, **xs: f(*args)

def assoc(m, key, val):
    """Copy-on-write associates a value in a dict"""
    cpy = deepcopy(m)
    cpy[key] = val
    return cpy


def associn(m, path, value):
    """ Copy-on-write associates a value in a nested dict """
    def assoc_recursively(m, path, value):
        if not path:
            return value
        p = path[0]
        return assoc(m, p, assoc_recursively(m.get(p,{}), path[1:], value))
    return assoc_recursively(m, path, value)


def merge(*maps):
    """Merge all maps left to right"""
    copies = map(deepcopy, maps)
    return reduce(lambda acc, val: acc.update(val) or acc, copies)

