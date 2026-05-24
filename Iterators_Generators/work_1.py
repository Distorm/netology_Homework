class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.outer_idx = 0
        self.inner_idx = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.outer_idx < len(self.list_of_list):
            if self.inner_idx < len(self.list_of_list[self.outer_idx]):
                item = self.list_of_list[self.outer_idx][self.inner_idx]
                self.inner_idx += 1
                return item
            self.outer_idx += 1
            self.inner_idx = 0
        raise StopIteration


def test_1():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


if __name__ == '__main__':
    test_1()