import time


def pytest_runtest_call(item):
    time.sleep(1)
