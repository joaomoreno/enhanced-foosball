import unittest

class Node:
  def __init__(self, element):
    self.element = element
    self.next = None

class RingBuffer:
  def __init__(self, cap):
    self.cap = cap
    self.size = 0
    self.head = None
    self.tail = None

  def __len__(self):
    return self.size

  def __iter__(self):
    current = self.head
    tail = self.tail

    while current is not None and current != tail:
      yield current.element
      current = current.next
    
    if current is not None:
      yield current.element
  
  def push(self, element):
    node = Node(element)

    if self.size == 0:
      self.head = node
      self.tail = node
      self.size = 1
    else:
      self.tail.next = node
      self.tail = node
      self.size += 1
      
      while self.size > self.cap:
        self.head = self.head.next
        self.size -= 1

class TestRingBuffer(unittest.TestCase):

  def test_RingBuffer(self):
    buffer = RingBuffer(5)
    self.assertListEqual(list(buffer), [])
    buffer.push(0)
    self.assertListEqual(list(buffer), [0])
    buffer.push(1)
    self.assertListEqual(list(buffer), [0, 1])
    buffer.push(2)
    self.assertListEqual(list(buffer), [0, 1, 2])
    buffer.push(3)
    self.assertListEqual(list(buffer), [0, 1, 2, 3])
    buffer.push(4)
    self.assertListEqual(list(buffer), [0, 1, 2, 3, 4])
    buffer.push(5)
    self.assertListEqual(list(buffer), [1, 2, 3, 4, 5])
    buffer.push(6)
    self.assertListEqual(list(buffer), [2, 3, 4, 5, 6])
    buffer.push(7)
    self.assertListEqual(list(buffer), [3, 4, 5, 6, 7])

if __name__ == '__main__':
    unittest.main()