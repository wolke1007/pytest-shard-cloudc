"""Group C: 10 collection tests."""

import allure


@allure.feature("Group C")
@allure.story("List")
def test_c01(): assert [1, 2, 3][0] == 1                  # noqa: E704

@allure.feature("Group C")
@allure.story("List")
def test_c02(): assert sorted([3, 1, 2]) == [1, 2, 3]     # noqa: E704

@allure.feature("Group C")
@allure.story("List")
def test_c03(): assert list(reversed([1, 2, 3])) == [3, 2, 1]  # noqa: E704

@allure.feature("Group C")
@allure.story("Dict")
def test_c04(): assert {"a": 1}.get("a") == 1             # noqa: E704

@allure.feature("Group C")
@allure.story("Dict")
def test_c05(): assert {"a": 1}.get("b", 0) == 0          # noqa: E704

@allure.feature("Group C")
@allure.story("Dict")
def test_c06(): assert len({"x": 1, "y": 2}) == 2         # noqa: E704

@allure.feature("Group C")
@allure.story("Set")
def test_c07(): assert {1, 2} | {2, 3} == {1, 2, 3}       # noqa: E704

@allure.feature("Group C")
@allure.story("Set")
def test_c08(): assert {1, 2, 3} & {2, 3, 4} == {2, 3}    # noqa: E704

@allure.feature("Group C")
@allure.story("Tuple")
def test_c09(): assert (1, 2, 3)[1] == 2                   # noqa: E704

@allure.feature("Group C")
@allure.story("Tuple")
def test_c10(): assert len((1, 2, 3, 4, 5)) == 5           # noqa: E704
