"""Shard tests to support parallelism across multiple machines."""

import hashlib
from collections.abc import Iterable, Sequence

import pytest


def non_negative_int(x: int | str) -> int:
    x = int(x)
    if x < 0:
        raise ValueError(f"Argument {x} must be non-negative")
    return x


def positive_int(x: int | str) -> int:
    x = int(x)
    if x <= 0:
        raise ValueError(f"Argument {x} must be positive")
    return x


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add pytest-shard specific configuration parameters."""
    group = parser.getgroup("shard")
    group.addoption(
        "--shard-id",
        dest="shard_id",
        type=non_negative_int,
        default=0,
        help="Number of this shard.",
    )
    group.addoption(
        "--num-shards",
        dest="num_shards",
        type=positive_int,
        default=1,
        help="Total number of shards.",
    )


def pytest_report_collectionfinish(config: pytest.Config, items: Sequence[pytest.Item]) -> str:
    """Log how many and, if verbose, which items are tested in this shard."""
    msg = f"Running {len(items)} items in this shard"
    if config.option.verbose > 0 and config.getoption("num_shards") > 1:
        msg += ": " + ", ".join(item.nodeid for item in items)
    return msg


def sha256hash(x: str) -> int:
    return int.from_bytes(hashlib.sha256(x.encode()).digest(), "little")


def filter_items_by_shard(
    items: Iterable[pytest.Item], shard_id: int, num_shards: int
) -> Sequence[pytest.Item]:
    """Computes `items` that should be tested in `shard_id` out of `num_shards` total shards."""
    return [item for item in items if sha256hash(item.nodeid) % num_shards == shard_id]


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Mutate the collection to consist of just items to be tested in this shard."""
    shard_id = config.getoption("shard_id")
    shard_total = config.getoption("num_shards")
    if shard_id >= shard_total:
        raise ValueError(f"shard_id={shard_id} must be less than num_shards={shard_total}")

    items[:] = filter_items_by_shard(items, shard_id, shard_total)
