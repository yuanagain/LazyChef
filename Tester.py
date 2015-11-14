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


#Potential TODO (catch exception where recipe is empty)
numTasks =(0,0)
completeCtr = 0

def initializeRecipe():
    numTasks = (8,8)
    DG_dense = np.zeros(numTasks)
    Tnode0 = TaskNode(0,0,0,np.array([1,2,3,4]), \
                    'Put water on stove', \
                    'Put water in pot. Put pot on stove')
    Tnode1 = TaskNode(1,30,0,np.array([5]), \
                      'Put water on stove', \
                      'Put water in pot. Put pot on stove')
    Tnode2 = TaskNode(2,0,300,np.array([]), \
                      'Boil Water', \
                      'Bring water to a boil')
    Tnode3 = TaskNode(3,15,0,np.array([]), \
                      'Add salt', \
                      'Add salt to water')
    Tnode4 = TaskNode(4,15,0,np.array([]), \
                      'Put pasta in water', \
                      'Add pasta to boiling water')
    Tnode5 = TaskNode(5,60,0,np.array([6]), \
                      'Dice Tomatoes', \
                      'Dice Tomatoes into small cubes')
    Tnode6 = TaskNode(6,20,0,np.array([7]), \
                      'Drain pasta', \
                      'Drain pasta using a strainer')
    Tnode7 = TaskNode(7,15,0,np.array([]), \
                      'Put Tomatoes in pasta', \
                      'Cover the pasta with Tomatoes')

    #Use a dictionary to maintain connectivity between
    #TaskNode data and id
    dct = dict()
    dct[0] = Tnode0
    dct[1] = Tnode1
    dct[2] = Tnode2
    dct[3] = Tnode3
    dct[4] = Tnode4
    dct[5] = Tnode5
    dct[6] = Tnode6
    dct[7] = Tnode7
    for i in range(0,numTasks[0]):
    #    extract params
    #    Tnode = TaskNode(params)
    #    dct[i] = Tnode
        for k in range(0,len(dct[i].depends)):
           j = dct[i].depends[k]
           DG_dense[i][j] = 1  

    DG_sparse = csr_matrix(DG_dense)
    return DG_sparse

def getNewlyAccesibleTasks():
    return 0


def optimizeRecipe():
    DG_sparse = initializeRecipe()
    BForder = breadth_first_order(DG_sparse,0,\
                              return_predecessors=False)
    
    PQ = PriorityQueue(numTasks[0])
    PQ.put(dict[BForder[0]])
    
    while completeCtr < numTasks[0]:
        temp = PQ.get()
        execute(temp)
        completeCtr = completeCtr + 1

    return BForder
#    recipeCompleted = False
#    while !recipeCompleted:
#        recipe = initialize_recipe()
#        pQueue = Q.PriorityQueue()
#        accessible_array = get_new_accessible(graph)
#        for taskNode in accessible_array:
#            pQueue.put(taskNode)
#        node = pQueue.get()
#        node.execute()
        
def execute(tnode):
    tnode.state = "completed"


def main():
    initializeRecipe()
    #print(optimizeRecipe())

if __name__ == '__main__':
    main()
