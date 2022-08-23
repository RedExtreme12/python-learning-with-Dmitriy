from typing import Any, Union
from itertools import pairwise


class Node:

    def __init__(self, value: Union['Node', Any], next_: Union['Node', None] = None):
        self._next = self._value = None
        self.next = next_
        self.value = value

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next_: Union['Node', None]):
        self._next = next_

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: Union['Node', Any]):
        self._value = value

    def _flatten_nodes(self):
        current = self

        stack = [current]

        while stack:
            current = stack.pop()

            if not isinstance(current.value, Node):
                yield current

            if isinstance(current.value, Node):
                stack.append(current.next)
                current = current.value
            elif current.next is not None:
                current = current.next
            else:
                continue

            stack.append(current)

    def __iter__(self):
        return (node.value for node in self._flatten_nodes())

    def flatten(self) -> None:
        flattened_nodes = self._flatten_nodes()

        for node_pair in pairwise(flattened_nodes):
            node_pair[0].next = node_pair[1]


if __name__ == '__main__':
    r1 = Node(1)
    assert [1] == list(r1)

    r2 = Node(7, Node(2, Node(9)))
    assert [7, 2, 9] == list(r2)

    r3 = Node(3, Node(Node(19, Node(25)), Node(12)))
    assert [3, 19, 25, 12] == list(r3)

    r4 = Node(3, Node(Node(Node(12, Node(40)), Node(25)), Node(12)))
    assert [3, 12, 40, 25, 12] == list(r4)

    r4.flatten()

    r4_node = r4
    while r4_node is not None:
        assert not isinstance(r4_node.value, Node)
        r4_node = r4_node.next

