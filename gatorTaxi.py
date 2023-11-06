import sys,re
from rbtree import RBT
from minheap import minHeap

#rbt and min heap objects
r=RBT()
m=minHeap()
fname=sys.argv[1]

with open(fname+".txt",'r') as f, open('output_file.txt', 'w') as o:
    #reading file contents
    for line in f:

        val = re.split(r'\(|\)', line)[1:-1]

        i='Insert'
        g='GetNextRide'
        u='UpdateTrip'
        c='CancelRide'
        p='Print'

        #helper function for split by ','
        def help():
            arr=[]
            for x in val[0].split(','):
                if not x.isdigit():
                    arr.append(x)
                else:
                    arr.append(int(x))
            return arr

        #handles Insert case
        def case1():
            rn,rc,td=help()
            node=r.insert(rn,rc,td)
            #if node is not a leaf node then insert
            if node !=r.leaf:
                m.insert(rn,rc,td,node)

            # ride number already exists
            else:
                print('Duplicate RideNumber'+'\n')
                o.write('Duplicate RideNumber'+'\n')
                sys.exit()


        #handles print ride case
        def case2():
            a=help()
            #only one argument search for node with corresponding ride no.
            if len(a)==1:
                node=r.search(a[0])
                #when the node is not a leaf node
                if node!=r.leaf:
                    print((node.rideNumber,node.rideCost,node.tripDuration))
                    o.write(str((node.rideNumber,node.rideCost,node.tripDuration))+'\n')

                #no nodes in mentioned range
                else:
                    print((0,0,0))
                    o.write("(0, 0, 0)\n")
                    
            else:
                nodes=r.Print(a[0],a[1])
                if len(nodes)!=0:

                    print(", ".join(str(i) for i in nodes))
                    outline=",".join(str(node) for node in nodes)
                    o.write(outline+'\n')
                    
                else:
                    o.write("(0, 0, 0)\n")
                    

                
        #handles update trip case with given ride number
        def case3():
            
            rn,newtd=help()
            updatenode=r.search(rn)
            #passing node and new trip arguments
            m.updateTrip(updatenode,newtd)
            r.UpdateTrip(updatenode,newtd)

        #handles cancel ride case
        def case4():
            #search for node with given ride number to delete
            rn=int(val[0])
            delnode=r.search(rn)

            #if leaf node do nothing
            if delnode ==r.leaf:
                pass
            #call cancel ride
            else:

                m.cancelRide(delnode)
                r.CancelRide(delnode)

        #handles Get next ride case
        def case5():
            #return ride with smallest cost or break tie with duration
            nextRide=m.GetNextRide()

            # active ride case
            if nextRide is not None:
                r.CancelRide(nextRide[3])
                print((nextRide[0],nextRide[1],nextRide[2]))
                o.write(str((nextRide[0],nextRide[1],nextRide[2]))+'\n')
            # no active rides 
            else:
                print("No active ride requests")
                o.write("No active ride requests\n")

        #switch case type statements:

        if i in line:

            case1()

            
        elif p in line:

            case2()
           

        elif u in line:

            case3()
            
        elif c in line:
            case4()
            

        elif g in line:
            case5()
            

