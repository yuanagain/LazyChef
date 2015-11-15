"""
This module provides classes for loading a library of recipes.

CONTENTS:
============================================================
I. CLASSES

II. USEFUL METHODS

III. EXAMPLE USAGE:
============================================================

============================================================
I. CLASSES
============================================================

class recipeLibrary():

Description:
A library that loads defintions from disk and allows for extraction of
lists of tasks upon which the optimizer can act

============================================================
II. USEFUL METHODS
============================================================
    

__init__(self, def_list_dir = './recipe_files/'):
    Description:
    ------
    Creates a recipeLibrary object
    
    Parameters
    ------
    def_list_dir : fname (default =  ./recipe_files/')

        A list of defintion


extract_list(self, recipes):
    Description:
    ------
    Returns node_list of task nodes required to produce all tasks in recipes.

    The node_list follows the following rules

        node_list[0] := start TaskNode, upon which all ingredients depend
        node_list[1] := done TaskNode, which depends upon each recipe in recipes

        for K > 1
        node_list[ K ] := kth TaskNode required for completion

    Parameters
    ------
    recipes : list
        A list of recipes task_str's that must be completes


dump_file(self, outFile = None, show = True):
    Description:
    ------
    Writes library to JSON

    Parameters:
    ------
    outFile : filename (default = None)
        The destination of the data dump. Defaults to ./tasks_out/tasklist
        if outFile is not specified

    show : boolean (default = True)
        If True, prints contents to screen as well

============================================================
III. EXAMPLE USAGE:
============================================================

import taskNodeGeneratorUtils as tnUtils

recipe_lib = tnUtils.recipeLibrary()

target = ['Boil Water', 'Pasta']

node_list = recipe_lib.extract_list(target)
...
Sort node_list via optimizaiton methods
...






Author: Yuan Wang
Contact/Support: yuanw@princeton.edu

"""
import sys
import os
from os import listdir
from os.path import isfile, join
from tnode import TaskNode
import todoListGenerator as tdlg
import random

class recipeLibrary():
    def __init__(self, def_list_dir = './recipe_files/'):
        self.str_to_index = dict()
        self.str_to_node = dict()
        self.tnode_list = []

        def_list = [ f for f in listdir(def_list_dir) if isfile(join(def_list_dir, f)) ]

        index = 0

        for fname in def_list:
            with open(def_list_dir + fname) as f:
                content = f.readlines()
            # extract data
            task_str = content[0][:-1]
            task_desc = content[1][:-1]
            act_time = float(content[2])
            back_time = float(content[3])
            depends = content[4:]
            for i in range(len(depends)):
                if (depends[i][-1] == '\n'): depends[i] = depends[i][:-1]

            # add to list
            tnode = TaskNode(index, act_time, back_time, depends, task_str, task_desc)
            self.tnode_list.append(tnode)

            # update helper dicts
            self.str_to_index[task_str] = index
            self.str_to_node[task_str] = tnode

            index = index + 1

        # updating dependency indices

        for i in range(0, len(self.tnode_list)):
            tnode = self.tnode_list[i]

            tnode.depends = [self.str_to_index[el] for el in tnode.depends]




    def print_library(self):
        """
        prints all TaskNodes in library
        """
        tdlg.dump_print(self.tnode_list)

    def dump_file(self, outFile = None, show = True):
        """ 
        Description:
        ------
        Writes library to JSON

        Parameters:
        ------
        outFile : filename (default = None)
            The destination of the data dump. Defaults to ./tasks_out/tasklist
            if outFile is not specified

        show : boolean (default = True)
            If True, prints contents to screen as well
        """
        tdlg.tnodelist_tojson(self.tnode_list, outFile)
        if show:
            os.system("cat " + outFile)


    def extract_list(self, recipes):
        """
        Description:
        ------
        Returns node_list of task nodes required to produce all tasks in recipes.

        The node_list follows the following rules

            node_list[0] := start TaskNode, upon which all ingredients depend
            node_list[1] := done TaskNode, which depends upon each recipe in recipes

            for K > 1
            node_list[ K ] := kth TaskNode required for completion

        Parameters
        ------
        recipes : list
            A list of recipes task_str's that must be completes
        """
        
        node_list = []

        # creat start_node
        start_node = TaskNode(-1, 0.0, 0.0, [], "Start", "Unleash the Kraken")
        node_list.append(start_node)

        # create DONE node, with all desired recipes as dependency
        recipe_ids  = [self.str_to_index[el] for el in recipes]

        done_node = TaskNode(-1, 0.0, 0.0, recipe_ids, "Done", "Nice work")
        node_list.append(done_node)


        # relevant_nodes := a list of integers coresponding to indices of nodes 
        # per self.node_list, where nodes correspond to tasks that are required
        # by the recipes
        relevant_nodes = []    
        relevant_nodes = self.find_relevant(done_node, relevant_nodes)

        relevant_set = set(relevant_nodes)

        relevant_list = self.create_relevant_list(start_node, done_node, relevant_set)
        
        return relevant_list


    def create_relevant_list(self, start_node, done_node, relevant_set):
        """
        Create relevant list of nodes
        """

        ## Remap indices bijectively
        renumerate = dict()
        ctr = 2
        for index in relevant_set:
            if index == -1: continue
            renumerate[index] = ctr
            ctr = ctr + 1

        ## Apply mapping, populate list
        start_node.id = 0
        done_node.id = 1
        relevant_list = [start_node, done_node]

        for index in relevant_set:
            # clone node
            new_node = self.tnode_list[index].copy()

            # adjust id's
            new_node.id = renumerate[new_node.id]

            new_node.depends = [renumerate[dpd] for dpd in new_node.depends]

            # connect all raw ingredients to start node
            if len(new_node.depends) == 0:
                new_node.depends.append(0)

            relevant_list.append(new_node)

        return clean_list(relevant_list)

        

    def find_relevant(self, node, relevant_nodes):
        """
        Populates relevant_nodes with all nodes relevant to node; i.e.
        resursively adds all dependencies' id's of node to relevant_nodes
        """
        relevant_nodes.append(node.id)

        for index in node.depends:
            relevant_nodes = self.find_relevant(self.tnode_list[index], relevant_nodes)

        return relevant_nodes

def print_nodelist(node_list, validate = False):
    """ 
    for all nodes in node_list, it prints their task_str
    """
    for index, node in enumerate(node_list):

        if validate:
            print(index == node.id)
            if index != node.id: 
                print("===ANOMALY====")
                print(node.id)
                print(index)
                print(node.task_str)
                print(node.depends)
                print("=========")
        print(node.task_str)

def clean_list(node_list):
    """ 
    cleans out anomaly end node
    """
    if node_list[-1] != node_list[-1].id:
        return node_list[:-1]
    return node_list

def main():

    print("==== TESTING CONSTRUCTOR ==== ")

    target = ['Boil Water', 'Pasta']

    lib = recipeLibrary(def_list_dir = './test_recipes/')
    print("SUCCESS")
    print("\n==== PRINTING LIBRARY ==== ")
    lib.print_library()
    print('\n')
    print("==== + ==== + ==== + ==== ")
    print("SAVING CONTENTS TO: ./tasks_out/test_outfile.txt ")
    os.system("rm -rf ./tasks_out/test_outfile.txt")
    lib.dump_file(outFile = "./tasks_out/test_outfile.txt")

    print("\n==== ==== ==== ==== ")
    print("EXTRACTING RELEVANT TASKS FOR:")
    print(target)
    node_list = lib.extract_list(target)
    print("\n==== TASKS EXTRACTED ==== ")
    print_nodelist(node_list)
    print("\n==== RAW INGREDIENTS ==== ")
    for i in range(1, len(node_list)):
        node = node_list[i]
        if node.depends[0] == 0:
            print(node.task_str)

if __name__ == "__main__":
    main()