"""Demo: collection tests (20 tests)."""

import allure
import pytest


@allure.feature("Collections")
@allure.story("List")
class TestList:
    def test_append(self):
        lst = [1, 2]
        lst.append(3)
        assert lst == [1, 2, 3]

    def test_pop(self):
        lst = [1, 2, 3]
        assert lst.pop() == 3
        assert lst == [1, 2]

    def test_sort(self):
        lst = [3, 1, 2]
        lst.sort()
        assert lst == [1, 2, 3]

    def test_reverse(self):
        lst = [1, 2, 3]
        lst.reverse()
        assert lst == [3, 2, 1]

    def test_slice(self):
        lst = [0, 1, 2, 3, 4]
        assert lst[1:3] == [1, 2]


@allure.feature("Collections")
@allure.story("Dict")
class TestDict:
    def test_get(self):
        d = {"a": 1}
        assert d.get("a") == 1

    def test_get_default(self):
        d = {"a": 1}
        assert d.get("b", 0) == 0

    def test_keys(self):
        d = {"x": 1, "y": 2}
        assert set(d.keys()) == {"x", "y"}

    def test_update(self):
        d = {"a": 1}
        d.update({"b": 2})
        assert d == {"a": 1, "b": 2}

    def test_pop(self):
        d = {"a": 1, "b": 2}
        assert d.pop("a") == 1
        assert "a" not in d


@allure.feature("Collections")
@allure.story("Set")
class TestSet:
    def test_union(self):
        assert {1, 2} | {2, 3} == {1, 2, 3}

    def test_intersection(self):
        assert {1, 2, 3} & {2, 3, 4} == {2, 3}

    def test_difference(self):
        assert {1, 2, 3} - {2, 3} == {1}

    def test_in(self):
        assert 2 in {1, 2, 3}

    def test_add(self):
        s = {1, 2}
        s.add(3)
        assert s == {1, 2, 3}


@allure.feature("Collections")
@allure.story("Tuple")
class TestTuple:
    def test_index(self):
        t = (10, 20, 30)
        assert t[1] == 20

    def test_length(self):
        assert len((1, 2, 3)) == 3

    def test_unpack(self):
        a, b, c = (1, 2, 3)
        assert (a, b, c) == (1, 2, 3)

    def test_count(self):
        assert (1, 2, 2, 3).count(2) == 2

    def test_immutable(self):
        t = (1, 2, 3)
        with pytest.raises(TypeError):
            t[0] = 99  # type: ignore[index]
