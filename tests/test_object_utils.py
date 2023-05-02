from .test_utils import *
from tlbx.object_utils import initializer


class InitializeTest:
    @initializer
    def __init__(self, a, b, c, d=1, e=2, **kwargs):
        pass


def test_initializer():
    obj = InitializeTest(1, 2, 3, e=4, x=5)
    assert obj.a == 1
    assert obj.b == 2
    assert obj.c == 3
    assert obj.d == 1
    assert obj.e == 4
    assert obj.x == 5
