class Node:
 def __init__(self, elm,nxt):
   self.elm= elm
   self.nxt =nxt
class LQueue:
   def __init__(self):
      self.head= self.dummy =Node(None, None)
   def __bool__(self):
      return self.head is not self.dummy
   def push_back(self, x):
      self.dummy.elm, self.dummy.nxt = x,Node(None, None)
      self.dummy = self.dummy.nxt