class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            raise IndexError("Queue is empty.")

    def peek(self):
        if not self.is_empty():
            return self.items[0]
        else:
            raise IndexError("Queue is empty.")

    def size(self):
        return len(self.items)

    def __repr__(self):
        return "Queue(" + ", ".join(map(str, self.items)) + ")"


"""

    Start Linked List

"""


class LinkedList:

    class _Node:
        def __init__(self, data):
            self.data = data
            self.next = None

    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def append(self, data):
        new_node = self._Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def insert(self, prev_node, data):
        if not prev_node:
            raise ValueError("Previous node must be in the list.")
        new_node = self._Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete(self, key):
        curr_node = self.head
        if curr_node and curr_node.data == key:
            self.head = curr_node.next
            curr_node = None
            return
        prev_node = None
        while curr_node and curr_node.data != key:
            prev_node = curr_node
            curr_node = curr_node.next
        if not curr_node:
            return
        prev_node.next = curr_node.next
        curr_node = None

    def find(self, key):
        curr_node = self.head
        while curr_node:
            if curr_node.data == key:
                return curr_node
            curr_node = curr_node.next
        return None

    def __repr__(self):
        nodes = []
        curr_node = self.head
        while curr_node:
            nodes.append(str(curr_node.data))
            curr_node = curr_node.next
        return " -> ".join(nodes)


"""

    Start Stack

"""


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("Stack is empty.")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("Stack is empty.")

    def size(self):
        return len(self.items)

    def __repr__(self):
        return "Stack(" + ", ".join(map(str, self.items)) + ")"
