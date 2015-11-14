'''

Module Main:

    description: main module, features returnRecipe method where 
                 cook-time optimization algorithm is performed

    Variables (not all global):

        numTasks           : Number of tasks in this recipe [int]
        recipeName         : Name of the recipe being optimized
                             [String]
        recipeCompleted    : Are we done with the optimized 
                             recipe (ready to output?) [bool]
        recipe_out         : List of TaskNode objects in the
                             optimized order [list]
        PQ                 : Max Priority Queue for considering
                             TaskNodes, compared by
                             background time [PriorityQueue] 
        completeCtr        : Counter to determine if all TaskNodes
                             were completed [int]

    methods:

        initializeRecipe(input file):
            -Makes TaskNode objects from file
            -Create Directed graph of all TaskNodes to complete a 
            certain recipe from an input file
            -Returns the DiGraph as a sparse adjancency matrix

        optimizeRecipe(DiGraph):
            -Takes in the DiGraph from initializeRecipe, and runs 
            our optimization algorithm.
            -Returns the final list of objects in optimized order,
            i.e. recipe_out

        execute(TaskNode):
            -change state in "inProgress"
            -while (PQ.peek.back_time + elap_time) < back_time 
            increment elap_time

        main():
            -Tester client     

'''

from Queue import PriorityQueue
import numpy as np
from tnode import TaskNode
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import breadth_first_order
from scipy.sparse.csgraph import connected_components

#Potential TODO (catch exception where recipe is empty)
#numTasks =(0,0)
numTasks = (10,10)
DG_dense = np.zeros(numTasks)
recipe_out = []

#Queue of background tasks in progress
InProgQ = []

#Priority queue of tasks
PQ = PriorityQueue(numTasks[0])

#Global time (for assigning beginning times)
global_time = 0.0

#Use a dictionary to maintain connectivity between
#TaskNode data and id
dct = dict()

def initializeRecipe():
    Tnode0 = TaskNode(0,0,0,np.array([1,2,3,4,9]), \
                    'start', \
                    'startNode')
    Tnode0.state = "complete"
    Tnode1 = TaskNode(1,30,0,np.array([5,9]), \
                      'Put water on stove', \
                      'Put water in pot. Put pot on stove')
    Tnode2 = TaskNode(2,15,0,np.array([5,9]), \
                      'Add salt', \
                      'Add salt to water')
    Tnode3 = TaskNode(3,60,0,np.array([9]), \
                      'Dice Tomatoes', \
                      'Dice Tomatoes into small cubes')
    Tnode4 = TaskNode(4,15,0,np.array([9]), \
                      'Prepare Drink', \
                      'Prepare a drink on the side')
    Tnode5 = TaskNode(5,0,300,np.array([6,9]), \
                      'Boil Water', \
                      'Bring water to a boil')
    Tnode6 = TaskNode(6,15,0,np.array([7,9]), \
                      'Put pasta in water', \
                      'Add pasta to boiling water')
    Tnode7 = TaskNode(7,20,0,np.array([8,9]), \
                      'Drain pasta', \
                      'Drain the pasta with a strainer')
    Tnode8 = TaskNode(8,15,0,np.array([9]), \
                      'Put Tomatoes on pasta', \
                      'Cover the pasta with Tomatoes')
    Tnode9 = TaskNode(9,0,0,np.array([]), \
                      'done', \
                      'Done with recipe')

    dct[0] = Tnode0
    dct[1] = Tnode1
    dct[2] = Tnode2
    dct[3] = Tnode3
    dct[4] = Tnode4
    dct[5] = Tnode5
    dct[6] = Tnode6
    dct[7] = Tnode7
    dct[8] = Tnode8
    dct[9] = Tnode9
    for i in range(0,numTasks[0]):
    #    extract params
    #    Tnode = TaskNode(params)
    #    dct[i] = Tnode
        for k in range(0,len(dct[i].depends)):
           j = dct[i].depends[k]
           DG_dense[i][j] = 1  

    #Symmetrically flip DG_dense about diagonal to reverse Digraph
    #DG_dense_rev = np.zeros(numTasks)
    #for i in range(0, numTasks[0]):
    #    for j in range(0, numTasks[0]):
    #        DG_dense_rev[i][j] = DG_dense[j][i]

    #DG_sparse = csr_matrix(DG_dense)
    #return DG_sparse

def getNewlyAccesibleTasks(tnode):
    for i in tnode.depends:
        canPut = True
        #print("Current possible dependencies are : ")
        #print(tnode.depends)       
        for j in range(0,numTasks[0]):
            if DG_dense[j][i] == 1:
                #print("i is : " + str(i))
                #print("j is : " + str(j))
                #print(dct[j].state == "complete")
                if dct[j].state != "complete":
                    canPut = False
        if canPut == True:
            PQ.put(dct[i])
            #print("Just added " + dct[i].task_desc)
                    
    
def optimizeRecipe():
    initializeRecipe()
    cTask = dct[0]
    while cTask.task_str != "done":
        getNewlyAccesibleTasks(cTask)
        cTask = PQ.get()
        execute(cTask)

def execute(tnode):
    global global_time
    #print("Executing " + tnode.task_desc)
    recipe_out.append(tnode)
    tnode.beg_time = global_time
    if tnode.act_time > 0:
        completeTask(tnode)
        global_time = global_time + tnode.act_time
        for i in InProgQ:
            i.elap_time = i.elap_time + tnode.act_time
            #print("Elapsed time for task :" + str(i.elap_time))
            #print("Task : " + str(i.task_desc))
            #print("PQ is empty returns : " + str(PQ.empty() == True))
            #temp = PQ.get()
            #print("Just popped from PQ : " + temp.task_desc)
            #PQ.put(temp)
            if PQ.empty() == True:
                #print("Nothing on PQ")
                long_on_ProgQ = 0
                for j in InProgQ:
                    if j.back_time > long_on_ProgQ:
                        long_on_ProgQ = j.back_time
                    completeTask(j)
                global_time = global_time + long_on_ProgQ

            if inProgF(i) == False:
                 completeTask(i)
           
    elif tnode.back_time > 0:
        tnode.state = "inProgress"
        InProgQ.append(tnode)

def inProgF(tnode):
    assert(tnode.act_time == 0)
    if tnode.elap_time < tnode.back_time:
        return True
    else:
        return  False

def completeTask(tnode):
    #print("Entered completeTask")
    tnode.state = "complete"
    if tnode.back_time > 0:
        InProgQ.remove(tnode)
        getNewlyAccesibleTasks(tnode)
    #print(tnode.task_desc)  

def main():
    optimizeRecipe()
    for i in recipe_out:
        print(i.task_desc)
        print(i.beg_time)

if __name__ == '__main__':
    main()