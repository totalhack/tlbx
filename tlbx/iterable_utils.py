from functools import reduce
from itertools import chain, combinations
from operator import or_

from ordered_set import OrderedSet


def powerset(iterable):
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def chunks(l, chunksize):
    for i in range(0, len(l), chunksize):
        yield l[i : i + chunksize]


def nchunks(a, n):
    """Divide iterable a into n chunks"""
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n))


def read_chunks(reader, chunksize, limit=None):
    """Given an iterator/generator, read/yield chunks of chunksize up to
    (optional) limit"""
    chunk = []
    for i, line in enumerate(reader):
        if limit and i >= limit:
            break
        if i % chunksize == 0 and i > 0:
            yield chunk
            chunk = []
        chunk.append(line)
    yield chunk


def iter_or(iterable):
    return reduce(or_, iterable)


def orderedsetify(obj):
    """Take ordered iterable and turn it into OrderedSet"""
    if isinstance(obj, OrderedSet):
        return obj
    if isinstance(obj, (list, tuple)):
        return OrderedSet(obj)
    if isinstance(obj, dict):
        # Assumes keys are ordered!
        return OrderedSet(obj.keys())
    assert False, "Not sure how to setify %s" % obj
