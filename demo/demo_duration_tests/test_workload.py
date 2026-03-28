"""15 demo tests with varying simulated durations (see conftest.py)."""

import allure


@allure.feature("Workload")
@allure.story("Heavy")
def test_w01(): assert True  # noqa: E704

@allure.feature("Workload")
@allure.story("Light")
def test_w02(): assert True  # noqa: E704

@allure.feature("Workload")
@allure.story("Light")
def test_w03(): assert True  # noqa: E704

@allure.feature("Workload")
@allure.story("Heavy")
def test_w04(): assert True  # noqa: E704

@allure.feature("Workload")
@allure.story("Light")
def test_w05(): assert True  # noqa: E704

@allure.feature("Workload")
@allure.story("Light")
def test_w06(): assert True  # noqa: E704

@allure.feature("Workload")
@allure.story("Heavy")
def test_w07(): assert True  # noqa: E704

@allure.feature("Workload")
@allure.story("Light")
def test_w08(): assert True  # noqa: E704

@allure.feature("Workload")
@allure.story("Light")
def test_w09(): assert True  # noqa: E704

@allure.feature("Workload")
@allure.story("Heavy")
def test_w10(): assert True  # noqa: E704

@allure.feature("Workload")
@allure.story("Light")
def test_w11(): assert True  # noqa: E704

@allure.feature("Workload")
@allure.story("Light")
def test_w12(): assert True  # noqa: E704

@allure.feature("Workload")
@allure.story("Medium")
def test_w13(): assert True  # noqa: E704

@allure.feature("Workload")
@allure.story("Medium")
def test_w14(): assert True  # noqa: E704

@allure.feature("Workload")
@allure.story("Medium")
def test_w15(): assert True  # noqa: E704
