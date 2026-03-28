import time


def pytest_runtest_call(item):  # noqa: ARG001
    time.sleep(1)
