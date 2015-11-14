'''

Module: Task Node

  features class description of TaskNode


'''

import numpy as np

'''
class TaskNode:

description:
    
    Describes a task necessary to complete a recipe

attributes:
    act_time    : Active time (required by human) [double]
    back_time   : Background Time (not required by human) [double]
    elap_time   : Elapsed Time (used to determine task completion)
                  [double]
    state       : String representing current state of task
                  (toDo, inProgress, Completed) [String]
    id          : unique integer index of this task in graph
                  [int]
    depends     : List of Task Nodes dependent on completion
                  of parent Task Node
                  [List]
    task_str    : Task String (brief string identification of
                   task)
                  [String]
    task_desc   : Full task description as a string [String]              

    TODO: include a list of quantities so that task_desc can
    say something like "mix X of this and Y of that"

initializer input:
    id_in, act_time_in, back_time_in, depends_in, task_str_in,
    task_desc_in

methods:
    
'''

class TaskNode():
    def __init__(self,id_in, act_time_in, back_time_in, depends_in,\
                 task_str_in, task_desc_in):
        self.state = "toDo"
        self.elap_time = 0.0
        self.id = id_in
        self.act_time = act_time_in
        self.back_time = back_time_in
        self.depends = depends_in
        self.task_str = task_str_in
        self.task_desc = task_desc_in

def main():
  dependencies = np.array([1,2,3])
  Tnode = TaskNode(1,4.0,0.0,dependencies,'Chop onions',\
                    'Dice the onions to 0.5 mm^3 chunks')
  print(Tnode.state)
  print(Tnode.elap_time)
  print(Tnode.id)
  print(Tnode.act_time)
  print(Tnode.back_time)
  print(Tnode.depends)
  print(Tnode.task_str)
  print(Tnode.task_desc)

if __name__ == '__main__':
  main()
