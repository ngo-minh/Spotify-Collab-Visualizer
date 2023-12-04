# help from https://www.geeksforgeeks.org/max-heap-in-python/

class Heap:
    # constructor
    def __init__(self):
        self.heap = []

    # parent
    def parent(self, index):
        if index == 0:
            return 0
        else:
            return (index - 1) // 2
        
    # left
    def left_child(self, index):
        return 2 * index + 1
    
    # right
    def right_child(self, index):
        return 2 * index + 2

    # check if the heap is empty
    def is_empty(self):
        return len(self.heap) == 0

    # swap two elements in the heap
    def swap(self, index1, index2):
        temp = self.heap[index1]
        self.heap[index1] = self.heap[index2]
        self.heap[index2] = temp

    # isert an element into the heap 
    def insert(self, key):
        self.heap.append(key)
        current_index = len(self.heap) - 1
        while current_index > 0:
            parent_index = self.parent(current_index)
            if self.heap[current_index][0] > self.heap[parent_index][0]:
                self.swap(current_index, parent_index)
                current_index = parent_index
            else:
                break

    # extract the maximum element
    def extract_max(self):
        if len(self.heap) == 0:
            raise Exception("Heap is empty")
        if len(self.heap) == 1:
            return self.heap.pop()

        max_element = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify_down(0)
        return max_element
    
    # reorganize the heap
    def heapify_down(self, index):
        while True:
            left = self.left_child(index)
            right = self.right_child(index)
            largest = index

            if left < len(self.heap) and self.heap[left][0] > self.heap[largest][0]:
                largest = left
            if right < len(self.heap) and self.heap[right][0] > self.heap[largest][0]:
                largest = right

            if largest != index:
                self.swap(index, largest)
                index = largest
            else:
                break


