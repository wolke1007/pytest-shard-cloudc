"""Demo: comparison and boolean tests (20 tests)."""

import allure


@allure.feature("Comparisons")
@allure.story("Numeric")
class TestNumericComparisons:
    def test_equal(self):
        assert 1 == 1

    def test_not_equal(self):
        assert 1 != 2

    def test_less(self):
        assert 1 < 2

    def test_greater(self):
        assert 2 > 1

    def test_less_equal(self):
        assert 2 <= 2


@allure.feature("Comparisons")
@allure.story("Boolean")
class TestBooleanLogic:
    def test_and_true(self):
        assert True and True

    def test_and_false(self):
        assert not (True and False)

    def test_or_true(self):
        assert True or False

    def test_or_false(self):
        assert not (False or False)

    def test_not(self):
        assert not False


@allure.feature("Comparisons")
@allure.story("Identity & Membership")
class TestIdentityMembership:
    def test_is_none(self):
        x = None
        assert x is None

    def test_is_not_none(self):
        x = 1
        assert x is not None

    def test_in_list(self):
        assert 3 in [1, 2, 3]

    def test_not_in_list(self):
        assert 4 not in [1, 2, 3]

    def test_in_string(self):
        assert "py" in "python"


@allure.feature("Comparisons")
@allure.story("Edge Cases")
class TestEdgeCases:
    def test_none_equality(self):
        assert None == None  # noqa: E711

    def test_bool_is_int(self):
        assert True == 1  # noqa: E712
        assert False == 0  # noqa: E712

    def test_empty_is_falsy(self):
        assert not []
        assert not {}
        assert not ""

    def test_zero_is_falsy(self):
        assert not 0
        assert not 0.0

    def test_chained_comparison(self):
        x = 5
        assert 1 < x < 10
