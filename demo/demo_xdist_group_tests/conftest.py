import time

import pytest


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "xdist_group(name): assign test to a named group; all tests in the group "
        "land on the same shard when using --shard-mode=hash.",
    )


def pytest_runtest_call(item):  # noqa: ARG001
    time.sleep(0.4)
