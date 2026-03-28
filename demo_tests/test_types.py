"""Demo: type and built-in function tests (20 tests)."""

import allure


@allure.feature("Types")
@allure.story("Type Checking")
class TestTypeChecking:
    def test_isinstance_int(self):
        assert isinstance(1, int)

    def test_isinstance_str(self):
        assert isinstance("hello", str)

    def test_isinstance_list(self):
        assert isinstance([], list)

    def test_isinstance_multi(self):
        assert isinstance(1, (int, float))

    def test_type_equality(self):
        assert type(1) is int


@allure.feature("Types")
@allure.story("Type Conversion")
class TestTypeConversion:
    def test_int_to_str(self):
        assert str(42) == "42"

    def test_str_to_int(self):
        assert int("42") == 42

    def test_float_to_int(self):
        assert int(3.9) == 3

    def test_int_to_float(self):
        assert float(3) == 3.0

    def test_list_to_set(self):
        assert set([1, 2, 2, 3]) == {1, 2, 3}


@allure.feature("Types")
@allure.story("Built-ins")
class TestBuiltins:
    def test_abs(self):
        assert abs(-5) == 5

    def test_round(self):
        assert round(3.567, 2) == 3.57

    def test_min(self):
        assert min(3, 1, 2) == 1

    def test_max(self):
        assert max(3, 1, 2) == 3

    def test_sum(self):
        assert sum([1, 2, 3, 4, 5]) == 15


@allure.feature("Types")
@allure.story("Itertools-like")
class TestIterables:
    def test_enumerate(self):
        result = list(enumerate(["a", "b", "c"]))
        assert result == [(0, "a"), (1, "b"), (2, "c")]

    def test_zip(self):
        result = list(zip([1, 2], ["a", "b"]))
        assert result == [(1, "a"), (2, "b")]

    def test_map(self):
        assert list(map(str, [1, 2, 3])) == ["1", "2", "3"]

    def test_filter(self):
        assert list(filter(lambda x: x > 2, [1, 2, 3, 4])) == [3, 4]

    def test_sorted(self):
        assert sorted([3, 1, 2]) == [1, 2, 3]
