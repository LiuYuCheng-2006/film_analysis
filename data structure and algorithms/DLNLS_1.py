class Node:
  def __init__(self, elm):
    self.elm = elm

def insert_node(self, p, q):
        # insert p before q：把节点p插入到节点q前面
        p.nxt, p.prv = q, q.prv
        p.prv.nxt = p.nxt.prv = p


def insert_elm(self, x, q):
    p = Node(x)
    insert_node(p, q)


def delete_node(self, p):
    a = p.prv
    b = p.nxt
    a.nxt = b
    b.prv = a


def delete_elm(self, p):
    delete_node(p)
    return p.elm


class CLnLs:
    def __init__(self):
        self.dummy = Node(None)
        self.dummy.prv = self.dummy.nxt = self.dummy

    def __bool__(self):
        return self.dummy.nxt is not self.dummy

    def check_empty(self):
        if not self:
            raise IndexError

    def __iter__(self):
        p = self.dummy.nxt  # 从哑节点的下一个节点开始（链表第一个真实元素）
        while p is not self.dummy:  # 只要还没回到哑节点，就继续循环
            yield p.elm  # yield：生成器，返回当前节点的数据elm
            p = p.nxt  # p移动到下一个节点

    def __reversed__(self):
        p = self.dummy.prv  # 从哑节点的前一个节点开始（链表最后一个真实元素）
        while p is not self.dummy:  # 只要还没回到哑节点，就继续循环
            yield p.elm  # 返回当前节点的数据elm
            p = p.prv  # p移动到前一个节点

    def push(self, x):
        insert_elm(x, self.dummy.nxt)



    def pop(self):
      self.check_empty()
      x =delete_elm(self.dummy.nxt)
      return x
    def top(self):
      self.check_empty()
      return self.dummy.nxt.elm
    def push_back(self, x):
        insert_elm(x,self.dummy)
    def pop_back(self,x):
        self.check_empty()
        x=delete_elm(self.dummy.prv)
        return x
    def back(self):
        self.check_empty()

        return self.dummy.prv.elm

