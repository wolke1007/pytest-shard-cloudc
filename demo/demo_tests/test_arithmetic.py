"""Demo: arithmetic tests (20 tests)."""

import allure
import pytest


@allure.feature("Arithmetic")
@allure.story("Addition")
class TestAddition:
    def test_add_positive(self):
        assert 1 + 1 == 2

    def test_add_zero(self):
        assert 5 + 0 == 5

    def test_add_negative(self):
        assert 3 + (-3) == 0

    def test_add_floats(self):
        assert 0.1 + 0.2 == pytest.approx(0.3)

    def test_add_large(self):
        assert 10**6 + 10**6 == 2 * 10**6


@allure.feature("Arithmetic")
@allure.story("Subtraction")
class TestSubtraction:
    def test_sub_positive(self):
        assert 5 - 3 == 2

    def test_sub_zero(self):
        assert 7 - 0 == 7

    def test_sub_negative(self):
        assert 3 - (-2) == 5

    def test_sub_self(self):
        assert 42 - 42 == 0

    def test_sub_floats(self):
        assert 1.5 - 0.5 == pytest.approx(1.0)


@allure.feature("Arithmetic")
@allure.story("Multiplication")
class TestMultiplication:
    def test_mul_positive(self):
        assert 3 * 4 == 12

    def test_mul_zero(self):
        assert 999 * 0 == 0

    def test_mul_one(self):
        assert 7 * 1 == 7

    def test_mul_negative(self):
        assert (-3) * 4 == -12

    def test_mul_floats(self):
        assert 2.5 * 4 == pytest.approx(10.0)


@allure.feature("Arithmetic")
@allure.story("Division")
class TestDivision:
    def test_div_even(self):
        assert 10 / 2 == 5.0

    def test_div_float_result(self):
        assert 7 / 2 == pytest.approx(3.5)

    def test_floordiv(self):
        assert 7 // 2 == 3

    def test_modulo(self):
        assert 10 % 3 == 1

    def test_div_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError):
            _ = 1 / 0
