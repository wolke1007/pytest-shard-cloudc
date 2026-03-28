"""Group B: 10 string tests."""

import allure


@allure.feature("Group B")
@allure.story("Basics")
def test_b01(): assert len("hello") == 5          # noqa: E704

@allure.feature("Group B")
@allure.story("Basics")
def test_b02(): assert "hi" + "!" == "hi!"        # noqa: E704

@allure.feature("Group B")
@allure.story("Basics")
def test_b03(): assert "ab" * 3 == "ababab"       # noqa: E704

@allure.feature("Group B")
@allure.story("Case")
def test_b04(): assert "hello".upper() == "HELLO" # noqa: E704

@allure.feature("Group B")
@allure.story("Case")
def test_b05(): assert "WORLD".lower() == "world" # noqa: E704

@allure.feature("Group B")
@allure.story("Search")
def test_b06(): assert "hello".find("ll") == 2    # noqa: E704

@allure.feature("Group B")
@allure.story("Search")
def test_b07(): assert "hello".startswith("he")   # noqa: E704

@allure.feature("Group B")
@allure.story("Search")
def test_b08(): assert "hello".endswith("lo")     # noqa: E704

@allure.feature("Group B")
@allure.story("Transform")
def test_b09(): assert "  hi  ".strip() == "hi"   # noqa: E704

@allure.feature("Group B")
@allure.story("Transform")
def test_b10(): assert ",".join(["a","b","c"]) == "a,b,c"  # noqa: E704
