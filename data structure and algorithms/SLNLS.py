class Node:
 def __init__(self, elm,nxt):
   self.elm= elm
   self.nxt =nxt
class LnLs:
   def __init__(self):
     self.head= None
   def __bool__(self):
     return self.head is not None
   def top(self):
     if not self:
       raise IndexError
     return self.head.elm
   def push(self, x):
     p = Node(x, self.head)
     self.head = p
   def pop(self):
    x = self.top()
    self.head = self.head.nxt
    return x

   def index_of(self, x):
       for i, y in enumerate(self):
         if x == y:
           return i
       return -1

   def __getitem__(self, i):
       for j, x in enumerate(self):
         if i == j:
           return x
       raise IndexError

   def reverse(self):
       rev = LnLs()
       while self:
          rev.push(self.pop())
       self.head = rev.head

   def reverse(self):

    p, q = self.head, None

     # qpointstothepreviousnode

    while p is not None:

      t = p.nxt
      p.nxt = q
      q = p
      p = t

    self.head = q
