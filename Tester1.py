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
import taskNodeGeneratorUtils as tnUtils
from taskNodeGeneratorUtils import recipeLibrary
#from scipy.sparse import csr_matrix
#from scipy.sparse.csgraph import breadth_first_order
#from scipy.sparse.csgraph import connected_components

#Target recipe name
#target = ['add_salt','boil_water','dice_tomatoes',\
#          'drain_pasta','pasta_in_water','pot_on_stove',\
#          'prepare_drink','tomatoes_on_pasta']

target = ['Piggy Wiggy', 'Cocktail Sausages', 'Roll Dough',\
           'Wrap Sausages', 'Turn on Oven', 'Preheat Oven',\
            ]

#Create recipe library
#recipe_lib = recipeLibrary('./recipe_files/')
#recipe_lib = recipeLibrary('./test_recipes/')
recipe_lib = recipeLibrary('./more_recipes/')

#Node List
node_list = recipe_lib.extract_list(target)

'''
for i in range(0, len(node_list)):
    print(node_list[i].id)
    print(node_list[i].depends)
    print(node_list[i].state)
    print(node_list[i].task_str)
    print("================")
'''

#Initialize Digraph adjacency matrix to be of dimension
#(numTasks) on a side.
numTasks =(len(node_list),len(node_list))
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
    global DG_dense
    #global numTasks
    
    #Populate dictionary and adjacency matrix from node_list
    for i in range(0,numTasks[0]):
        dct[i] = node_list[i]
        #print(dct[i].depends)
        for k in range(0,len(dct[i].depends)):
           j = dct[i].depends[k]
           DG_dense[i][j] = 1  

    DG_dense = DG_dense.transpose()
    #print(DG_dense)
    
    #Rearrange dependencies in the dictionary to 
    #reflect reversed Digraph
    for j in range(0, numTasks[0]):
        newDep = []
        for i in range(0, numTasks[0]):
            if DG_dense[j][i] == 1:
                newDep.append(i) 
        dct[j].depends = newDep
     
    dct[0].state = "complete"
    
    
    print("+++++++++++++++++++++++++")
    for i in range(0, len(node_list)):
        print(dct[i].id)
        print(dct[i].depends)
        print(dct[i].state)
        print(dct[i].task_str)
        print("================")
    

def getNewlyAccesibleTasks(tnode):
    for i in tnode.depends:
        canPut = True
        print("Current possible dependencies are : ")
        print(tnode.depends)       
        for j in range(0,numTasks[0]):
            if DG_dense[j][i] == 1:
                print("i is : " + str(i))
                print("j is : " + str(j))
                print(dct[j].state != "complete")
                if dct[j].state != "complete":
                    if j != tnode.id:
                        #print("Self-Match pruned")
                        canPut = False
                        break
        if canPut == True:
            PQ.put(dct[i])
            print("Just added " + dct[i].task_str)
                    
def optimizeRecipe(): 
    initializeRecipe()
    cTask = dct[0]
    while cTask.task_str != "done":
        getNewlyAccesibleTasks(cTask)
        cTask = PQ.get()
        execute(cTask)
    return recipe_out

def execute(tnode):
    global global_time
    print("Executing " + tnode.task_str)
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
                    print(j.task_str)
                    if j.back_time > long_on_ProgQ:
                        long_on_ProgQ = j.back_time
                    completeTask(j)
                global_time = global_time + long_on_ProgQ

            if inProgF(i) == False and self.PQ.empty() != True:
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
    print("completed " + tnode.task_str)
    tnode.state = "complete"
    if tnode.back_time > 0:
        for i in InProgQ:
            print("test : " + i.task_str)
        InProgQ.remove(tnode)
        #getNewlyAccesibleTasks(tnode)
    #print(tnode.task_desc)  

def main():
    optimizeRecipe()
    for i in recipe_out:
        print(i.task_desc)
        print(i.beg_time)

if __name__ == '__main__':
    main()
