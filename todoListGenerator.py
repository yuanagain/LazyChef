"""
This module provides methods for exporting data from
a list of TaskNodes to JSON

The primary function of interest of this file is
tnodelist_tojson, which allows the user to generate
json file todo items from a list of TaskNodes.

CONTENTS:
============================================================
I. USEFUL METHODS

II. EXAMPLE USAGE:
============================================================

============================================================
I. USEFUL METHODS
============================================================

tnodelist_todict(tnode_list):
    Parameters:
    ------
    Takes a list of TaskNodes and returns a dict of ordered tasks
    ------
    tnode_list : TaskNode[]
        A list of TaskNodes


tnodelist_tojson(tnode_list, out_fname = None):
    Parameters:
    ------
    Takes a list of TaskNodes and produces a json file at out_fname
    ------
    tnode_list : TaskNode[]
        A list of TaskNodes

    out_fname : Str (optional)
        The output json filname. Defaults to 
        "./tasks_out/tasklist<XYZ>.txt", where <XYZ> is an integer

============================================================
II. EXAMPLE USAGE:
============================================================

## import thisclass
import todoListGenerator as tdlg

## Generate raw lists
import taskNodeGeneratorUtils as tnUtils

recipe_lib = tnUtils.recipeLibrary()
target = ['Boil Water', 'Pasta']
node_list = recipe_lib.extract_list(target)

## Optimize list
...
Optimize node_list
...

## Export list to file
tdlg.tnode_list(node_list, out_fname = 'batch_job_001.json')

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






Author: Yuan Wang
Contact/Support: yuanw@princeton.edu

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

def tnodelist_todict(tnode_list):
    """
    Parameters:
    ------
    Takes a list of TaskNodes and returns a dict of ordered tasks
    ------
    tnode_list : TaskNode[]
        A list of TaskNodes

    """

    task_pack = generate_todo_list(tnode_list)

    return task_pack

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