from functools import reduce
from itertools import chain, combinations
from operator import or_

from orderedset import OrderedSet

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def chunk(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def iter_or(iterable):
    return reduce(or_, iterable)

def orderedsetify(obj):
    '''Take ordered iterable and turn it into OrderedSet'''
    if isinstance(obj, OrderedSet):
        return obj
    if isinstance(obj, (list, tuple)):
        return OrderedSet(obj)
    assert False, 'Not sure how to setify %s' % obj
