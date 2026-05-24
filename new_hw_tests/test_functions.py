import pytest
from functions import is_palindrome, sum_of_digits, reverse_string


@pytest.mark.parametrize("text, expected", [
    ("А роза упала на лапу Азора", True),
    ("hello", False),
    ("12321", True),
    ("", True),
    ("Was it a car or a cat I saw?", True),
    ("No 'x' in Nixon", True)
])
def test_is_palindrome(text, expected):
    assert is_palindrome(text) == expected


@pytest.mark.parametrize("number, expected", [
    (123, 6),
    (0, 0),
    (-456, 15),
    (9999, 36),
    (100000, 1)
])
def test_sum_of_digits(number, expected):
    assert sum_of_digits(number) == expected


@pytest.mark.parametrize("text, expected", [
    ("hello", "olleh"),
    ("Python", "nohtyP"),
    ("", ""),
    ("12345", "54321"),
    ("racecar", "racecar")
])
def test_reverse_string(text, expected):
    assert reverse_string(text) == expected