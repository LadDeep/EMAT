import pytest


class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("division by zero")
        return a / b



# @pytest.fixture
# def calculator():
#     return Calculator()


def test_add(calculator):
    assert calculator.add(2, 3) == 5
    assert calculator.add(-2, 3) == 1
    assert calculator.add(0, 0) == 0


def test_subtract(calculator):
    assert calculator.subtract(5, 2) == 3
    assert calculator.subtract(5, 5) == 0
    assert calculator.subtract(-5, -2) == -3


def test_multiply(calculator):
    assert calculator.multiply(2, 3) == 6
    assert calculator.multiply(0, 5) == 0
    assert calculator.multiply(-2, 4) == -8


def test_divide(calculator):
    assert calculator.divide(6, 3) == 2
    assert calculator.divide(5, 2) == pytest.approx(2.5)
    with pytest.raises(ZeroDivisionError):
        calculator.divide(10, 0)


def test_add_floats(calculator):
    assert calculator.add(2.5, 3.7) == pytest.approx(6.2)


def test_subtract_floats(calculator):
    assert calculator.subtract(5.2, 2.1) == pytest.approx(3.1)


def test_multiply_floats(calculator):
    assert calculator.multiply(2.5, 3.5) == pytest.approx(8.75)


def test_divide_floats(calculator):
    assert calculator.divide(7.5, 2) == pytest.approx(3.75)
    assert round(calculator.divide(10, 3.3), 2) == pytest.approx(3.03)


def test_divide_by_zero(calculator):
    with pytest.raises(ZeroDivisionError):
        calculator.divide(10, 0)
