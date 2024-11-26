from node import Node

class LLStack:

    def __init__(self):
        self.__head: Node = None
        self.__size: int = 0

    @property
    def size(self):
        return self.__size

    def pop(self) -> tuple:
        if self.__head is None:
            raise IndexError

        old_head = self.__head
        new_head = self.__head.next
        self.__head = new_head
        self.__size -= 1
        # This may not be needed
        old_head.next = None
        return old_head.data

    def push(self, data: tuple):
        if not isinstance(data, tuple):
            raise TypeError
        n = 0
        for i in data:
            n += 1
            if i < 0:
                raise ValueError
            if not isinstance(i, int):
                raise TypeError
        # n is number of values in tuple
        if n != 2:
            raise ValueError

        if self.__head is None:
            self.__head = Node(data)
        else:
            old_head = self.__head
            self.__head = Node(data)
            self.__head.next = old_head
        self.__size += 1

    def __str__(self):
        if self.__head is None:
            return ''
        i = self.__head
        r_str = ''
        while i.next is not None:
            # adds str data in-front of r_str so ordering is from oldest to newest
            r_str = str(i.data) + r_str
            r_str = ' -> ' + r_str
            i = i.next
        r_str = str(i.data) + r_str
        return r_str


# tll = LLStack()
# print(tll)
# tll.push((0, 0))
# print(tll)
# tll.push((0, 1))
# print(tll)
# tll.push((1, 1))
# tll.push((2, 1))
# print(tll)
# r = tll.pop()
# print(tll)
# print('pop: ', r)
#




