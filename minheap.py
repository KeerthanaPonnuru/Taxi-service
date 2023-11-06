from collections import deque
from rbtree import RBT

class minHeap():
    def __init__(self) -> None:
        self.s=0             #size
        self.list=[]         #ride requests list
        self.maps={}         #heap
        self.activeride=2000 #max active rides

    #insert new ride into min-heap
    def insert(self,rn,rc,td,rbnode):
        self.list.append([rn,rc,td,rbnode])
        i=len(self.list)-1
        self.maps[rbnode]=i
        self.ascend(i)
        return

    #find the index of the ride request
    def getIndex(self,rn):
        for key,t in enumerate(self.list):
            if rn==t[0]:
                return key
        return -1

    #update trip request based on the time duration
    def updateTrip(self,u,newtd):
        key=self.maps[u]
        #case a
        if newtd<=self.list[key][2]:
            self.list[key][2]=newtd
            self.ascend(key)
            newind=self.maps[u]
            self.descend(newind)
        #case b
        elif self.list[key][2]<newtd<=2*self.list[key][2]:
            self.list[key][1]+=10
            self.list[key][2]=newtd
            self.ascend(key)
            newind=self.maps[u]
            self.descend(newind)
        #case c
        elif newtd>2*self.list[key][2]:
            self.cancelRide(u)

    #cancel request and update it in the RB tree link node as well
    def cancelRide(self,node):
        key=self.maps[node]
        key2=self.list[key]

        #if ride request is not last use descend for min-heap property
        if key!=-1:
            if key==len(self.list)-1:
                del self.maps[key2[3]]
                self.list.pop()
            else:
                self.maps[self.list[-1][3]]=self.maps[key2[3]]
                del self.maps[key2[3]]
                self.list[key]=self.list.pop()
                self.descend(key)

    #min-heap property restoring by swapping with parent
    def ascend(self,i):

        if i>0 and (self.list[i][1]<self.list[(i-1)//2][1] or (self.list[i][1]==self.list[(i-1)//2][1] and self.list[i][2]<self.list[(i-1)//2][2])):
            self.list[i],self.list[(i-1)//2]=self.list[(i-1)//2],self.list[i]
            self.maps[self.list[i][3]],self.maps[self.list[(i-1)//2][3]]=self.maps[self.list[(i-1)//2][3]],self.maps[self.list[i][3]]
            self.ascend((i-1)//2)
        return
    #return ride request 
    def GetNextRide(self):
        if not self.list:
            return
        #check if active rides <2000 or not
        if len(self.list) > self.activeride:
            print('More than 2000 active rides')
        #if only one ride request remove directly
        if len(self.list)==1:
            del self.maps[self.list[-1][3]]
            ans=self.list.pop()
        #more than one ride request case
        else:
            ans=self.list[0]
            del self.maps[self.list[0][3]]
            self.maps[self.list[-1][3]]=0
            self.list[0]=self.list.pop()
            self.descend(0)
        return ans

    #min heap property restore by swapping with largest child
    def descend(self,i):
        m=2*i
        l=m+1
        r=m+2
        largest=i
        if l<len(self.list) and ((self.list[l][1]<self.list[largest][1]) or (self.list[l][1]==self.list[largest][1] and self.list[l][2]<self.list[largest][2])):
            largest=l
        if r<len(self.list) and ((self.list[r][1]<self.list[largest][1]) or (self.list[r][1]==self.list[largest][1] and self.list[r][2]<self.list[largest][2])):
            largest=r
        if largest!=i:
            self.list[i],self.list[largest]=self.list[largest],self.list[i]
            self.maps[self.list[i][3]],self.maps[self.list[largest][3]]=self.maps[self.list[largest][3]],self.maps[self.list[i][3]]
            self.descend(largest)
        return

