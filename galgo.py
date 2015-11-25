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

class GraphAlgo:
    def __init__(self, tasklist):
        self.node_list = tasklist
        
        #Initialize Digraph adjacency matrix to be of dimension
        #(numTasks) on a side.
        self.numTasks =(len(self.node_list),len(self.node_list))
        self.DG_dense = np.zeros(self.numTasks)
        self.recipe_out = []

        #Queue of background tasks in progress
        self.InProgQ = []

        #Priority queue of tasks
        self.PQ = PriorityQueue(self.numTasks[0])

        #Global time (for assigning beginning times)
        self.global_time = 0.0

        #Use a dictionary to maintain connectivity between
        #TaskNode data and id
        self.dct = dict()

    def initializeRecipe(self):
        #global DG_dense
        #global numTasks
        
        '''
        for i in range(0, len(self.node_list)):
            print(self.node_list[i].id)
            print(self.node_list[i].depends)
            print(self.node_list[i].state)
            print(self.node_list[i].task_str)
            print("================")
        '''

        #Populate dictionary and adjacency matrix from node_list
        for i in range(0,self.numTasks[0]):

            #If TaskNode has 0 active and background time, it's
            #an ingredient. Add it to the dictionary of ingredients
            #within the tasknode that depends on this tasknode
            #if self.node_list[i].back_time == 0 and \
            #    self.node_list[i].act_time == 0:

            self.dct[i] = self.node_list[i]
            #print(dct[i].depends)
            for k in range(0,len(self.dct[i].depends)):
               j = self.dct[i].depends[k]
               self.DG_dense[i][j] = 1  

        self.DG_dense = self.DG_dense.transpose()
        print(self.DG_dense)
        
        #Rearrange dependencies in the dictionary to 
        #reflect reversed Digraph
        for j in range(0, self.numTasks[0]):
            newDep = []
            for i in range(0, self.numTasks[0]):
                if self.DG_dense[j][i] == 1:
                    newDep.append(i) 
            self.dct[j].depends = newDep
         
        self.dct[0].state = "complete"

        
        print("+++++++++++++++++++++++++")
        for i in range(0, len(self.node_list)):
            print(self.dct[i].id)
            print(self.dct[i].depends)
            print(self.dct[i].state)
            print(self.dct[i].task_str)
            print(self.dct[i].act_time)
            print(self.dct[i].back_time)
            print("================")
           

    def getNewlyAccesibleTasks(self, tnode):
        for i in tnode.depends:
            canPut = True
            print("Current possible dependencies are : ")
            print(tnode.depends)       
            for j in range(0, self.numTasks[0]):
                if self.DG_dense[j][i] == 1:
                    print("i is : " + str(i))
                    print("j is : " + str(j))
                    print(self.dct[j].state != "complete")
                    if self.dct[j].state != "complete":
                        #if j != tnode.id:
                            #print("Self-Match pruned")
                            canPut = False
                            break
            if canPut == True:
                self.PQ.put(self.dct[i])
                print("Just added " + self.dct[i].task_str)
                        
    def optimizeRecipe(self): 
        self.initializeRecipe()
        cTask = self.dct[0]
        while cTask.task_str != "done":
            self.getNewlyAccesibleTasks(cTask)
            cTask = self.PQ.get()
            self.execute(cTask)
        return self.recipe_out

    def execute(self, tnode):
        #global global_time
        print("Executing " + tnode.task_str)
        self.recipe_out.append(tnode)
        tnode.beg_time = self.global_time
        if tnode.act_time > 0:
            self.completeTask(tnode)
            self.global_time = self.global_time + tnode.act_time
            for i in self.InProgQ:
                i.elap_time = i.elap_time + tnode.act_time
                #print("Elapsed time for task :" + str(i.elap_time))
                #print("Task : " + str(i.task_desc))
                #print("PQ is empty returns : " + str(PQ.empty() == True))
                #temp = PQ.get()
                #print("Just popped from PQ : " + temp.task_desc)
                #PQ.put(temp)
                if self.PQ.empty() == True:
                    print("Nothing on PQ")
                    long_on_ProgQ = 0
                    for j in self.InProgQ:
                        #print("WTF " + j.task_str)
                        if j.back_time > long_on_ProgQ:
                            long_on_ProgQ = j.back_time
                        self.completeTask(j)
                    self.global_time = self.global_time + long_on_ProgQ

                if self.inProgF(i) == False and self.PQ.empty() != True:
                     self.completeTask(i)
               
        elif tnode.back_time > 0:
            tnode.state = "inProgress"
            self.InProgQ.append(tnode)
        else: #tnode.back_time == 0 and tnode.act_time == 0:
            #print("THIRD IF")
            self.completeTask(tnode) 

            
    def inProgF(self, tnode):
        assert(tnode.act_time == 0)
        if tnode.elap_time < tnode.back_time:
            return True
        else:
            return False

    def completeTask(self, tnode):
        #print("completed " + tnode.task_str)
        tnode.state = "complete"
        if tnode.back_time > 0:
            self.InProgQ.remove(tnode)
            #for i in self.InProgQ:
                #print("test : " + i.task_str)
            
