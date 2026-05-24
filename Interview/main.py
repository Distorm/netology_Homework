class Stack:

    def __init__(self) -> None:
        self._items: list = []

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def push(self, item) -> None:
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def size(self) -> int:
        return len(self._items)


def check_balanced(brackets_string: str) -> str:
    stack = Stack()

    # Словарь для быстрого поиска пары: закрывающая -> открывающая
    matching_bracket = {
        ')': '(',
        ']': '[',
        '}': '{'
    }

    open_brackets = set(matching_bracket.values())
    close_brackets = set(matching_bracket.keys())

    for char in brackets_string:
        if char in open_brackets:
            stack.push(char)

        elif char in close_brackets:
            if stack.is_empty():
                return "Несбалансированно"

            top_element = stack.pop()

            if matching_bracket[char] != top_element:
                return "Несбалансированно"

    if stack.is_empty():
        return "Сбалансированно"
    else:
        return "Несбалансированно"


if __name__ == '__main__':
    test_cases = [
        ("(((([]]))))", "Сбалансированно"),
        ("[([])((([[[]]])))]{()}", "Сбалансированно"),
        ("{{[()]}}", "Сбалансированно"),
        ("}{}", "Несбалансированно"),
        ("{{[(])]}}", "Несбалансированно"),
        ("[[{())}]", "Несбалансированно"),
        ("((())", "Несбалансированно"),
    ]

    print("Запуск тестов:")
    for test_str, expected in test_cases:
        result = check_balanced(test_str)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{test_str}' -> {result} (ожидалось: {expected})")