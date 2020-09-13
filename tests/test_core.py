import pytest

from tlbx.core_utils import raiseif, raiseifnot


def test_raiseif():
    with pytest.raises(AssertionError):
        raiseif(1 != 2)


def test_raiseifnot():
    with pytest.raises(AssertionError):
        raiseifnot(1 == 2)
