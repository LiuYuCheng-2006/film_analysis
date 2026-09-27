class AStack:
   def __init__(self):
     self.a=[]
   def __bool__(self):
     return self.a!=[]
   def top(self):
    return self.a[-1]
   def push(self, x):
     self.a.append(x)
   def pop(self):
     x = self.top()
     del self.a[-1]
     return x
def paren_match(s):
   st =AStack()
   for c in s:
     if c in ('(', '[', '{'):
       st.push(c)
     elif c in (')', ']', '}'):
       if not st or st.pop()+c not in ('()', '[]', '{}'):
          return False
   return not st
class AQueue:
   def __init__(self):
     self.a=[None]*16
     self.n= len(self.a)
     self.head= self.tail =0

   def __bool__(self):
     return self.head!= self.tail

   def __len__(self):
     return (self.tail-self.head)%self.n

   def __iter__(self):
     yield from (self.a[(self.head+i)%self.n] for i in range(len(self)))

   def top(self):
     if not self:
        raise IndexError
     return self.a[self.head]


   def pop(self):
      x = self.top()
      self.a[self.head] = None
      self.head = (self.head + 1) % self.n
      return x


   def push_back(self, x):

     l = len(self)

     if l + 1 == self.n:  # back-endlistisfull
       self.a[self.tail:self.tail] = [None] * self.n
       self.n = len(self.a)
       self.head = (self.tail - l) % self.n
     self.a[self.tail] = x
     self.tail = (self.tail + 1) % self.n