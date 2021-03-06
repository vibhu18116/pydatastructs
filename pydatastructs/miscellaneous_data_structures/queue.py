from pydatastructs.linear_data_structures import DynamicOneDimensionalArray, SinglyLinkedList
from pydatastructs.utils.misc_util import NoneType, LinkedListNode
from copy import deepcopy as dc

__all__ = [
    'Queue'
]

class Queue(object):
    """Representation of queue data structure.

    Parameters
    ==========

    implementation : str
        Implementation to be used for queue.
        By default, 'array'
    items : list/tuple
        Optional, by default, None
        The inital items in the queue.
    dtype : A valid python type
        Optional, by default NoneType if item
        is None.

    Examples
    ========

    >>> from pydatastructs import Queue
    >>> q = Queue()
    >>> q.append(1)
    >>> q.append(2)
    >>> q.append(3)
    >>> q.popleft()
    1
    >>> len(q)
    2

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Queue_(abstract_data_type)
    """

    def __new__(cls, implementation='array', **kwargs):
        if implementation == 'array':
            return ArrayQueue(
                kwargs.get('items', None),
                kwargs.get('dtype', int))
        elif implementation == 'linkedlist':
            return LinkedListQueue(
                kwargs.get('items', None),
                kwargs.get('dtype', NoneType)
            )
        raise NotImplementedError(
                "%s hasn't been implemented yet."%(implementation))

    def append(self, *args, **kwargs):
        raise NotImplementedError(
            "This is an abstract method.")

    def popleft(self, *args, **kwargs):
        raise NotImplementedError(
            "This is an abstract method.")

    @property
    def is_empty(self):
        raise NotImplementedError(
            "This is an abstract method.")


class ArrayQueue(Queue):

    __slots__ = ['front']

    def __new__(cls, items=None, dtype=NoneType):
        if items is None:
            items = DynamicOneDimensionalArray(dtype, 0)
        else:
            dtype = type(items[0])
            items = DynamicOneDimensionalArray(dtype, items)
        obj = object.__new__(cls)
        obj.items, obj.front = items, -1
        if items.size == 0:
            obj.front = -1
        else:
            obj.front = 0
        return obj

    def append(self, x):
        if self.is_empty:
            self.front = 0
            self.items._dtype = type(x)
        self.items.append(x)

    def popleft(self):
        if self.is_empty:
            raise ValueError("Queue is empty.")
        return_value = dc(self.items[self.front])
        front_temp = self.front
        if self.front == self.rear:
            self.front = -1
        else:
            if (self.items._num - 1)/self.items._size < \
                self.items._load_factor:
                self.front = 0
            else:
                self.front += 1
        self.items.delete(front_temp)
        return return_value

    @property
    def rear(self):
        return self.items._last_pos_filled

    @property
    def is_empty(self):
        return self.__len__() == 0

    def __len__(self):
        return self.items._num

    def __str__(self):
        _data = []
        for i in range(self.front, self.rear + 1):
            _data.append(self.items._data[i])
        return str(_data)


class LinkedListQueue(Queue):

    __slots__ = ['front', 'rear', 'size', '_dtype']

    def __new__(cls, items=None, dtype=NoneType):
        obj = object.__new__(cls)
        obj.queue = SinglyLinkedList()
        obj._dtype = dtype
        if items is None:
            pass
        elif type(items) in (list, tuple):
            if len(items) != 0 and dtype is NoneType:
                obj._dtype = type(items[0])
            for x in items:
                if type(x) == obj._dtype:
                    obj.queue.append(x)
                else:
                    raise TypeError("Expected %s but got %s"%(obj._dtype, type(x)))
        else:
            raise TypeError("Expected type: list/tuple")
        obj.front = obj.queue.head
        obj.rear = obj.queue.tail
        obj.size = obj.queue.size
        return obj

    def append(self, x):
        if self._dtype is NoneType:
            self._dtype = type(x)
        elif type(x) is not self._dtype:
            raise TypeError("Expected %s but got %s"%(self._dtype, type(x)))
        self.size += 1
        self.queue.append(x)
        if self.front is None:
            self.front = self.queue.head
        self.rear = self.queue.tail

    def popleft(self):
        if self.is_empty:
            raise ValueError("Queue is empty.")
        self.size -= 1
        return_value = self.queue.pop_left()
        self.front = self.queue.head
        self.rear = self.queue.tail
        return return_value

    @property
    def is_empty(self):
        return self.size == 0

    def __len__(self):
        return self.size

    def __str__(self):
        return str(self.queue)
