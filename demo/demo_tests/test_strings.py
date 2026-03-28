"""Demo: string tests (20 tests)."""

import allure


@allure.feature("Strings")
@allure.story("Basics")
class TestStringBasics:
    def test_length(self):
        assert len("hello") == 5

    def test_empty(self):
        assert len("") == 0

    def test_concatenation(self):
        assert "foo" + "bar" == "foobar"

    def test_repetition(self):
        assert "ab" * 3 == "ababab"

    def test_in_operator(self):
        assert "ell" in "hello"


@allure.feature("Strings")
@allure.story("Case")
class TestStringCase:
    def test_upper(self):
        assert "hello".upper() == "HELLO"

    def test_lower(self):
        assert "WORLD".lower() == "world"

    def test_title(self):
        assert "hello world".title() == "Hello World"

    def test_swapcase(self):
        assert "Hello".swapcase() == "hELLO"

    def test_capitalize(self):
        assert "hello world".capitalize() == "Hello world"


@allure.feature("Strings")
@allure.story("Search & Replace")
class TestStringSearch:
    def test_find(self):
        assert "hello".find("ll") == 2

    def test_find_missing(self):
        assert "hello".find("xyz") == -1

    def test_replace(self):
        assert "foo bar foo".replace("foo", "baz") == "baz bar baz"

    def test_startswith(self):
        assert "hello".startswith("hel")

    def test_endswith(self):
        assert "hello".endswith("llo")


@allure.feature("Strings")
@allure.story("Split & Join")
class TestStringSplitJoin:
    def test_split(self):
        assert "a,b,c".split(",") == ["a", "b", "c"]

    def test_split_default(self):
        assert "a b  c".split() == ["a", "b", "c"]

    def test_join(self):
        assert ",".join(["a", "b", "c"]) == "a,b,c"

    def test_strip(self):
        assert "  hello  ".strip() == "hello"

    def test_splitlines(self):
        assert "a\nb\nc".splitlines() == ["a", "b", "c"]
