class HashTableEntry:
    """
    Hash Table entry, as a linked list node.
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def insert(self, key, value):
        while True:
            if self.key == key:
                self.value = value
                return False
            elif self.next:
                self = self.next
            else:
                self.next = HashTableEntry(key, value)
                return True

    def delete(self, key):
        if self.key == key:
            return self.next
        else:
            head = self
            while self.next is not None and self.key is not key:
                prev = self
                self = self.next
            prev.next = self.next
            return head

    def find(self, key):
        while self:
            if self.key == key:
                return self.value
            if self.next is None:
                return None
            else:
                self = self.next


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        self.capacity = capacity  # Number of buckets in the hash table
        self.initial_capacity = capacity
        self.storage = [None] * capacity
        self.size = 0

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.put(key, value)

    def fnv1(self, key):
        """
        FNV-1 64-bit hash function

        Implement this, and/or DJB2.
        """
        hash = 0xcbf29ce484222325
        fnvprime = 0x100000001b3
        fnvsize = 2**62
        if not isinstance(s, bytes):
            s = s.encode("UTF-8", "ignore")
        for byte in s:
            hash = (hash * fnvprime) % fnvsize
            hash = hash ^ byte
        return hash

    def djb2(self, key):
        """
        DJB2 32-bit hash function

        Implement this, and/or FNV-1.
        """
        hash = 5381
        for x in key:
            hash = ((hash << 5) + hash) + ord(x)
        return hash & 0xFFFFFFFF

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        # return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        # Find new elements index in the hash table
        newElementIndex = self.hash_index(key)
        # If that position is taken, insert it at the end of the linked list
        if self.storage[newElementIndex]:
            if self.storage[newElementIndex].insert(key, value):
                self.size += 1
        # else, assign new node to empty position
        else:
            self.storage[newElementIndex] = HashTableEntry(key, value)
            self.size += 1
        self.resize()

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        index = self.hash_index(key)
        if self.storage[index] is not None:
            self.storage[index] = self.storage[index].delete(key)
            self.size -= 1
        if self.storage[index] is None:
            print('Key not found')
        self.resize()

    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        index = self.hash_index(key)
        return self.storage[index].find(key) if self.storage[index] else None

    def __resize_to(self, size):
        newTable = HashTable(size)
        for slt in self.storage:
            if slt:
                current = slt
                while current:
                    newTable.put(current.key, current.value)
                    current = current.next
        self.capacity = newTable.capacity
        self.storage = newTable.storage

    def resize(self):
        """
        Doubles the capacity of the hash table and
        rehash all key/value pairs.

        Implement this.
        """
        load_factor = self.size/self.capacity
        if load_factor > 0.7:
            self.__resize_to(self.capacity*2)
        elif self.capacity > self.initial_capacity and load_factor < 0.2:
            self.__resize_to(self.capacity//2)


if __name__ == "__main__":
    ht = HashTable(2)

    ht.put("line_1", "Tiny hash table")
    ht.put("line_2", "Filled beyond capacity")
    ht.put("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.get("line_1"))
    print(ht.get("line_2"))
    print(ht.get("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize()
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.get("line_1"))
    print(ht.get("line_2"))
    print(ht.get("line_3"))

    print("")
