"""Group A: 10 arithmetic tests."""

import allure


@allure.feature("Group A")
@allure.story("Addition")
def test_a01(): assert 1 + 1 == 2        # noqa: E704

@allure.feature("Group A")
@allure.story("Addition")
def test_a02(): assert 2 + 2 == 4        # noqa: E704

@allure.feature("Group A")
@allure.story("Addition")
def test_a03(): assert 10 + 0 == 10      # noqa: E704

@allure.feature("Group A")
@allure.story("Subtraction")
def test_a04(): assert 5 - 3 == 2        # noqa: E704

@allure.feature("Group A")
@allure.story("Subtraction")
def test_a05(): assert 0 - 1 == -1       # noqa: E704

@allure.feature("Group A")
@allure.story("Multiplication")
def test_a06(): assert 3 * 4 == 12       # noqa: E704

@allure.feature("Group A")
@allure.story("Multiplication")
def test_a07(): assert 7 * 0 == 0        # noqa: E704

@allure.feature("Group A")
@allure.story("Division")
def test_a08(): assert 10 // 3 == 3      # noqa: E704

@allure.feature("Group A")
@allure.story("Division")
def test_a09(): assert 10 % 3 == 1       # noqa: E704

@allure.feature("Group A")
@allure.story("Power")
def test_a10(): assert 2 ** 8 == 256     # noqa: E704
