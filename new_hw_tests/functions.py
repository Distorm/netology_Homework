def is_palindrome(text: str) -> bool:
    cleaned = ''.join(char.lower() for char in text if char.isalnum())
    return cleaned == cleaned[::-1]


def sum_of_digits(number: int) -> int:
    return sum(int(digit) for digit in str(abs(number)))


def reverse_string(text: str) -> str:
    return text[::-1]