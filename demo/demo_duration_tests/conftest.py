"""conftest for demo_duration_tests: simulates varying test execution times."""

import time

# Predetermined "random" durations (1-10 s) designed to be severely unbalanced
# under round-robin but near-perfectly balanced under duration mode.
#
# Round-robin with 3 shards sorts by nodeid and assigns by index % 3:
#   shard 0 → test_w01,w04,w07,w10,w13  = 10+9+8+7+6 = 40 s
#   shard 1 → test_w02,w05,w08,w11,w14  =  1+1+1+1+2 =  6 s
#   shard 2 → test_w03,w06,w09,w12,w15  =  1+1+1+1+2 =  6 s
#
# LPT bin-packing on [10,9,8,7,6,2,2,1,1,1,1,1,1,1,1] → ~[18,17,17] s
_DURATIONS: dict[str, int] = {
    "test_w01": 10,
    "test_w02": 1,
    "test_w03": 1,
    "test_w04": 9,
    "test_w05": 1,
    "test_w06": 1,
    "test_w07": 8,
    "test_w08": 1,
    "test_w09": 1,
    "test_w10": 7,
    "test_w11": 1,
    "test_w12": 1,
    "test_w13": 6,
    "test_w14": 2,
    "test_w15": 2,
}


def pytest_runtest_call(item) -> None:  # noqa: ANN001
    time.sleep(_DURATIONS.get(item.name, 1))
