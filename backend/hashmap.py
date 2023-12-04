# help from https://www.geeksforgeeks.org/hash-map-in-python/

class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashMap:

    def __init__(self, size=100):
        self.size = size
        self.buckets = []
        for i in range(self.size):
            self.buckets.append(None)

    # method to generate a hash
    def get_hash(self, key):
        hash_sum = 0
        key_string = str(key)
        for character in key_string:
            hash_sum += ord(character)
        return hash_sum % self.size

    # add a key-value pair
    def set(self, key, value):
        index = self.get_hash(key)
        if self.buckets[index] is None:
            self.buckets[index] = HashNode(key, value)
        else:
            current_node = self.buckets[index]
            while True:
                if current_node.key == key:
                    current_node.value = value
                    break
                if current_node.next is None:
                    current_node.next = HashNode(key, value)
                    break
                current_node = current_node.next

    # get the value for a given key
    def get(self, key):
        index = self.get_hash(key)
        current_node = self.buckets[index]
        while current_node is not None:
            if current_node.key == key:
                return current_node.value
            current_node = current_node.next
        return None

    # delete a key-value pair
    def delete(self, key):
        index = self.get_hash(key)
        current_node = self.buckets[index]
        previous_node = None
        while current_node is not None:
            if current_node.key == key:
                if previous_node is None:
                    self.buckets[index] = current_node.next
                else:
                    previous_node.next = current_node.next
                break
            previous_node = current_node
            current_node = current_node.next
