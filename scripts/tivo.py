import unittest

class Node:
  def __init__(self, element):
    self.element = element
    self.next = None

def iterateTiVo(tivo):
  current = tivo.head
  tail = tivo.tail

  while current is not None and current != tail:
    yield current.element
    current = current.next
  
  if current is not None:
    yield current.element

class TiVo:
  def __init__(self, cap):
    self.cap = cap
    self.size = 0
    self.head = None
    self.tail = None

  def __len__(self):
    return self.size

  def __iter__(self):
    return iterateTiVo(self)
  
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

class TestTiVo(unittest.TestCase):

  def test_tivo(self):
    tivo = TiVo(5)
    self.assertListEqual(list(tivo), [])
    tivo.push(0)
    self.assertListEqual(list(tivo), [0])
    tivo.push(1)
    self.assertListEqual(list(tivo), [0, 1])
    tivo.push(2)
    self.assertListEqual(list(tivo), [0, 1, 2])
    tivo.push(3)
    self.assertListEqual(list(tivo), [0, 1, 2, 3])
    tivo.push(4)
    self.assertListEqual(list(tivo), [0, 1, 2, 3, 4])
    tivo.push(5)
    self.assertListEqual(list(tivo), [1, 2, 3, 4, 5])
    tivo.push(6)
    self.assertListEqual(list(tivo), [2, 3, 4, 5, 6])
    tivo.push(7)
    self.assertListEqual(list(tivo), [3, 4, 5, 6, 7])

if __name__ == '__main__':
    unittest.main()