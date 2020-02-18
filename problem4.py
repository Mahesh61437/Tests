"""

This program is a LRU cache system, which stores date in key value pairs
The least used cache memory will always be at the end of the cache memory

So when the capacity of the Cache is full and want to store a key, value
we just have to delete the last element


"""

class QNode(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

    def __str__(self):
        return "(%s, %s)" % (self.key, self.value)


class Cache(object):
    def __init__(self, capacity):

        if capacity <= 0:
            raise ValueError("capacity > 0")
        self.hash_map = {}
        self.head = None
        self.end = None

        self.capacity = capacity
        self.current_size = 0

    def get(self, key):
        """ function to get a key,value pair in the cache """

        if key not in self.hash_map:
            return -1

        node = self.hash_map[key]

        if self.head == node:
            return node.value
        self.remove(node)
        self.set_head(node)
        return node.value

    def insert(self, key, value):
        """ function to add a key,value pair to the cache """

        if key in self.hash_map:
            node = self.hash_map[key]
            node.value = value

            if self.head != node:
                self.remove(node)
                self.set_head(node)
        else:
            new_node = QNode(key, value)
            if self.current_size == self.capacity:
                del self.hash_map[self.end.key]
                self.remove(self.end)
            self.set_head(new_node)
            self.hash_map[key] = new_node

    def set_head(self, node):
        """ function to set the head pointer """
        if not self.head:
            self.head = node
            self.end = node
        else:
            node.prev = self.head
            self.head.next = node
            self.head = node
        self.current_size += 1

    def remove(self, node):
        """ function to remove a key,value pair from the cache """
        if not self.head:
            return

        # removing the node from the list
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev

        # if there is no elements, then set head and end to None
        if not node.next and not node.prev:
            self.head = None
            self.end = None

        # if node == end, update the new end
        if self.end == node:
            self.end = node.next
            self.end.prev = None
        self.current_size -= 1
        return node

    def print_elements(self):
        n = self.head
        print("[head = %s, end = %s]" % (self.head, self.end), end=" \n")
        while n:
            print("%s -> " % (n), end="")
            n = n.prev
        print("NULL")


if __name__ == '__main__':
    cacheObject = Cache(5)
    cacheObject.insert('a',1)
    cacheObject.insert('b', 2)
    cacheObject.insert('c', 3)
    cacheObject.insert('d', 4)
    cacheObject.print_elements()
    cacheObject.insert('b', 5)
    cacheObject.insert('e', 6)
    cacheObject.insert('f', 10)
    cacheObject.print_elements()
