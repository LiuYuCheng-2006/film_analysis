from fontTools.varLib.mutator import curr


class SingleNode:
    def __init__(self, item):
        self.item = item
        self.next = None
class singlelinkedlist:
    def __init__(self,node=None):
        self.head = node
    def isempty(self):
        return self.head is None
    def length(self):
        cur=self.head
        count=0
        while cur is not None:
            count+=1
            cur=cur.next
        return count
    def travel(self):
        cur=self.head
        while cur is not None:
            print(f'数值域{cur.item}')
            cur=cur.next
    def add(self,item):
        new_node = SingleNode(item)
        new_node.next = self.head
        self.head = new_node
    def append(self,item):
        new_node = SingleNode(item)
        if self.isempty():
            self.head=new_node
        else:
            cur=self.head
            while cur.next is not None:
                cur=cur.next
            cur.next = new_node
    def insert(self,pos,item):
        if pos<=0:
            self.add(item)
        elif pos>=self.length():
            self.append(item)
        else:
            cur=self.head
            count=0
            while count<pos-1:
                cur=cur.next
                count+=1
            new_node = SingleNode(item)
            new_node.next = cur.next
            cur.next = new_node
    def remove(self,item):
        cur=self.head
        pre=None
        while cur is not None:
            if cur.item == item:
                if cur==self.head:
                   self.head=cur.next

                else:
                    pre.next=cur.next
                return
            else:
                pre=cur
                cur=cur.next
    def search(self,item):
        cur=self.head
        while cur is not None:
            if cur.item == item:
                return True

            cur=cur.next
        return False



if __name__=="__main__":
    # node1 =SingleNode(1)
    my_linkedlist =  singlelinkedlist()
    print(f'头结点为{my_linkedlist.head}')
    # print(f'头结点数值域{my_linkedlist.head.item}')
    # print(f'头结点地址域{my_linkedlist.head.next}')
    print(my_linkedlist.isempty())
    my_linkedlist.add('a')
    my_linkedlist.add('b')
    my_linkedlist.append(1)
    my_linkedlist.append(2)
    my_linkedlist.insert(6,'f')
    print(my_linkedlist.length())

    my_linkedlist.remove('b')
    my_linkedlist.travel()



