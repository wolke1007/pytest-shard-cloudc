"""Test pytest_shard.pytest_shard."""

import collections
import itertools
from types import SimpleNamespace

from hypothesis import given, strategies
import pytest

from pytest_shard import pytest_shard


@given(strategies.integers(min_value=1))
def test_positive_int_with_pos(x):
    assert pytest_shard.positive_int(x) == x
    assert pytest_shard.positive_int(str(x)) == x


def test_non_negative_int_accepts_zero():
    assert pytest_shard.non_negative_int(0) == 0
    assert pytest_shard.non_negative_int("0") == 0


@given(strategies.integers(max_value=0))
def test_positive_int_with_neg(x):
    with pytest.raises(ValueError):
        pytest_shard.positive_int(x)
    with pytest.raises(ValueError):
        pytest_shard.positive_int(str(x))


def test_positive_int_with_non_num():
    invalid = ["foobar", "x1", "1x"]
    for s in invalid:
        with pytest.raises(ValueError):
            pytest_shard.positive_int(s)


@given(strategies.text())
def test_sha256hash_deterministic(s):
    x = pytest_shard.sha256hash(s)
    y = pytest_shard.sha256hash(s)
    assert x == y
    assert isinstance(x, int)


@given(strategies.text(), strategies.text())
def test_sha256hash_no_clash(s1, s2):
    if s1 != s2:
        assert pytest_shard.sha256hash(s1) != pytest_shard.sha256hash(s2)


MockItem = collections.namedtuple("MockItem", "nodeid")


@given(
    names=strategies.lists(strategies.text(), unique=True),
    num_shards=strategies.integers(min_value=1, max_value=500),
)
def test_filter_items_by_shard(names, num_shards):
    items = [MockItem(name) for name in names]

    filtered = [
        pytest_shard.filter_items_by_shard(items, shard_id=i, num_shards=num_shards)
        for i in range(num_shards)
    ]
    all_filtered = list(itertools.chain(*filtered))
    assert len(all_filtered) == len(items)
    assert set(all_filtered) == set(items)


def test_pytest_collection_modifyitems_rejects_invalid_shard_id():
    config = SimpleNamespace(getoption=lambda name: {"shard_id": 2, "num_shards": 2}[name])

    with pytest.raises(ValueError, match=r"shard_id=2 must be less than num_shards=2"):
        pytest_shard.pytest_collection_modifyitems(config, [])


def test_pytest_report_collectionfinish_with_verbose_output():
    config = SimpleNamespace(
        option=SimpleNamespace(verbose=1),
        getoption=lambda name: {"num_shards": 2}[name],
    )
    items = [MockItem("test_module.py::test_first"), MockItem("test_module.py::test_second")]

    message = pytest_shard.pytest_report_collectionfinish(config, items)

    assert message == (
        "Running 2 items in this shard: test_module.py::test_first, test_module.py::test_second"
    )
