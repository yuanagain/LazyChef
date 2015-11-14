"""
TODO: test functionalities
===================
The primary function of interest of this file is
tnodelist_tojson, which allows the user to generate
json file todo items from a list of TaskNodes.

def tnodelist_tojson(tnode_list, out_fname = None):
    Parameters:
    ------
    Takes a list of TaskNodes and produces a json file at out_fname
    ------
    tnode_list : TaskNode[]
        A list of TaskNodes

    out_fname : Str (optional)
        The output json filname. Defaults to 
        "./tasks_out/tasklist<XYZ>.txt", where <XYZ> is an integer


===================
AUX DEV NOTES
===================
task_pack['active']
task_pack['passive']

task_dict['name']
task_dict['start_time']
task_dict['end_time']
task_dict['time_delta']
task_dict['descripton']
"""

from tnode import TaskNode
import sys
import json
import random

gap_time = 3.0

def createTask(tnode, current_time = 0.0):
    """
    Parameters
    ------
    tnode : TaskNode
        The TaskNode being stripped
    current_time : double (default = 0.0)
        The time elapsed in seconds, useful in list construction

    ------
    This method extracts the important information from the node.
    Returns a dictionary of said information
    """

    task_dict = dict()
    task_dict['name'] = tnode.task_str
    task_dict['start_time'] = current_time
    task_dict['end_time'] = current_time + tnode.act_time
    task_dict['time_delta'] = max(tnode.act_time, tnode.back_time)
    task_dict['description'] = tnode.task_desc

    return task_dict

def tnodelist_tojson(tnode_list, out_fname = None):
    """
    Parameters:
    ------
    Takes a list of TaskNodes and produces a json file at out_fname
    ------
    tnode_list : TaskNode[]
        A list of TaskNodes

    out_fname : Str (optional)
        The output json filname. Defaults to 
        "./tasks_out/tasklist<XYZ>.txt", where <XYZ> is an integer
    """

    if out_fname == None:
        out_fname = "./tasks_out/tasklist" + str(random.randint(100, 999)) + ".json"

    task_pack = generate_todo_list(tnode_list)

    with open(out_fname, 'w') as outfile:
        json.dump(task_pack, outfile, indent=4)

def dump_print(tnode_list):
    task_pack = generate_todo_list(tnode_list)
    print(json.dumps(task_pack))

def generate_todo_list(tnode_list):
    """
    Parameters
    ------
    tnode_list : TaskNode[]
        A list of TaskNodes
    ------
    Turns a list of nodes into a batch of dictionaries with 
    information relevant to the web interface
    """
    active_task_list = []
    passive_task_list = []
    current_time = 0.0

    for tnode in tnode_list:
        
        task = createTask(tnode, current_time)
        current_time = current_time + tnode.act_time

        if tnode.act_time == 0.0:
            passive_task_list.append(task)
        else:
            active_task_list.append(task)

    task_pack = {'active': active_task_list, 'passive': passive_task_list}
    return task_pack

def main():
    print("MAIN NOT YET IMPLEMENTED")

if __name__ == "__main__":
    main()