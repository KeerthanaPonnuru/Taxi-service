
from collections import deque

#node in tree with attributes 
class Node:
    def __init__(self, rideNumber,rideCost,tripDuration):
        self.rideNumber = rideNumber
        self.rideCost=rideCost
        self.tripDuration=tripDuration
        self.p = None #parent
        self.c = None #color
        self.l = None #left
        self.r = None #right

    def colors(self):
        if self.c == 'BLACK':
            return 'BLACK'
        return 'RED'


class RBT:
    def __init__(self):
        self.leaf = Node(-1,-1,-1) 
        self.leaf.c = 'BLACK'
        self.leaf.l = None
        self.leaf.r = None
        self.root = self.leaf

    # rotate left for balancing
    def rot_l(self, node):
        y = node.r
        node.r = y.l 
        #check leaf node or not
        if y.l == self.leaf:
            pass
        else:
            y.l.p = node
        
        y.p = node.p 

        if node.p is None:
            self.root = y
        elif node == node.p.l:
            node.p.l = y
        else:
            node.p.r = y 

        y.l = node 
        node.p = y

    #rotate right for balancing
    def rot_r(self, node):
        y = node.l 
        node.l = y.r 

        #check leaf node or not
        if y.r == self.leaf:
            pass
        else:
            y.r.p = node

        y.p = node.p 

        if node.p is None:
            self.root = y 
        elif node == node.p.r:
            node.p.r = y 
        else:
            node.p.l = y 

        y.r = node 
        node.p = y

    #insert new node into tree
    def insert(self,rideNumber,rideCost,tripDuration):
        #check for position to insert node
        checknode=self.search(rideNumber)
        if checknode!=self.leaf:
            return self.leaf
        n = Node(rideNumber,rideCost,tripDuration)
        n.l = self.leaf
        n.r = self.leaf

        y = None 
        x = self.root
        #check if leaf node 
        while x != self.leaf:
            y = x
            if n.rideNumber < x.rideNumber:
                x = x.l 
            else:
                x = x.r 
        
        n.p = y 
        if y == None:
            self.root = n 
        elif n.rideNumber < y.rideNumber: 
            y.l = n 
        else:
            y.r = n

        self.insert_h(n)
        return n

    #helper function to maintain red-black property while delete node is performed
    def insert_h(self, n):
        while n.p and n.p.c == 'RED':
            #when parents is a right child
            if n.p != n.p.p.l:
                y = n.p.p.l 
                if y.c == 'RED':
                    n.p.c = 'BLACK'
                    y.c = 'BLACK'
                    n.p.p.c = 'RED'
                    n = n.p.p
                else:
                    if n == n.p.l:
                        n = n.p 
                        self.rot_r(n)
                    n.p.c = 'BLACK'
                    n.p.p.c = 'RED' 
                    self.rot_l(n.p.p)
            #when parent is a left child
            else:
                y = n.p.p.r 
                if y.c == 'RED':
                    n.p.c = 'BLACK'
                    y.c = 'BLACK' 
                    n.p.p.c = 'RED'
                    n = n.p.p
                else:
                    if n == n.p.r:
                        n = n.p 
                        self.rot_l(n)
                    n.p.c = 'BLACK'
                    n.p.p.c = 'RED' 
                    self.rot_r(n.p.p)
                
            if n == self.root:
                break
        self.root.c = 'BLACK'

    #remove node from tree
    def CancelRide(self, node):
        #check not leaf node
        if node != self.leaf:
            pass
        else:
            return

        y = node
        temp=node
        #existing node color
        initial = y.c 

        # case1
        if node.r == self.leaf:
            x = node.l
            self.exchange(node, node.l)
        #case2
        elif node.l == self.leaf:
            x = node.r 
            self.exchange(node, node.r)
        # case3
        else:
            y = self.minimum(node.r)
            initial = y.c
            x = y.r 
            
            if y.p == node:
                x.p = y
            else:
                self.exchange(y, y.r)
                y.r = node.r
                y.r.p = y
            
            self.exchange(node, y)
            y.l = node.l 
            y.l.p = y 
            y.c = node.c 
        
        if initial == 'BLACK':
            self.CancelRide_h(x)
        return temp
    #helper function to maintain red-black property while delete node is performed
    def CancelRide_h(self, x):
        while x != self.root and x.c == 'BLACK':
            if x == x.p.l:
                v = x.p.r
                # case 1
                if v.c == 'RED':
                    v.c = 'BLACK'
                    x.p.c = 'RED'
                    self.rot_l(x.p)
                    v = x.p.r
                # case 2
                if v.l.c == 'BLACK' and v.r.c == 'BLACK':
                    v.c = 'RED' 
                    x = x.p 
                else:
                    # case 3
                    if v.r.c == 'BLACK':
                        v.l.c = 'BLACK'
                        v.c = 'RED'
                        self.rot_r(v)
                        v = x.p.r
                    # case 4
                    v.c = x.p.c 
                    x.p.c = 'BLACK' 
                    v.r.c = 'BLACK' 
                    self.rot_l(x.p)
                    x = self.root
            else:
                v = x.p.l
                # case 'RED'
                if v.c == 'RED':
                    v.c = 'BLACK'
                    x.p.c = 'RED'
                    self.rot_r(x.p)
                    v = x.p.l
                # case 2
                if v.r.c == 'BLACK' and v.l.c == 'BLACK':
                    v.c = 'RED' 
                    x = x.p 
                else:
                    # case 3
                    if v.l.c == 'BLACK':
                        v.r.c = 'BLACK'
                        v.c = 'RED'
                        self.rot_l(v)
                        v = x.p.l
                    # case 4
                    v.c = x.p.c 
                    x.p.c = 'BLACK' 
                    v.l.c = 'BLACK' 
                    self.rot_r(x.p)
                    x = self.root
        x.c = 'BLACK'

    # O('RED')
    def exchange(self, u, v):
        if u.p == None:
            self.root = v
        elif u == u.p.l:
            u.p.l = v 
        else:
            u.p.r = v
        v.p = u.p 

    # O(h) = O(logn) 
    def minimum(self, x):
        while x.l != self.leaf:
            x = x.l
        return x

    # O(h) = O(logn) 
    def search(self, rnval):
        node = self.root
        while node != self.leaf and rnval != node.rideNumber:
            if rnval < node.rideNumber:
                node = node.l
            else:
                node = node.r
        return node
    
    #print triplets
    
    def Print(self,rn1,rn2):
        arr=[]
        self.print_help(arr,self.root,rn1,rn2)
        return arr
    
    #print all triplets between rn1 and rn2
    def print_help(self,arr,node,rn1,rn2):
        if node!=self.leaf:
            if node.rideNumber<rn1:
                self.print_help(arr,node.r,rn1,rn2)
            elif node.rideNumber>rn2:
                self.print_help(arr,node.l,rn1,rn2)
            else:
                self.print_help(arr,node.l,rn1,rn2)
                if node.rideNumber>=rn1 and node.rideNumber<=rn2:
                    arr.append((node.rideNumber,node.rideCost,node.tripDuration))
                self.print_help(arr,node.r,rn1,rn2)
    
    def UpdateTrip(self,ridenum,newtd):
        #case a:
        if newtd<=ridenum.tripDuration:
            ridenum.tripDuration=newtd
        #case b:
        elif ridenum.tripDuration<=newtd<=2*ridenum.tripDuration:
            ridenum.rideCost+=10
            ridenum.tripDuration=newtd
        #case c:
        elif newtd>2*ridenum.tripDuration:
            self.CancelRide(ridenum)

   
