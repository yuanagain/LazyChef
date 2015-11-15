"""
This module provides classes for providing a task sequence

CONTENTS:
============================================================
I. USEFUL METHODS
II. EXAMPLE USAGE:
============================================================

============================================================
I. USEFUL METHODS
============================================================

maximizer(node):

	Description:
	------
	Returns the optimal ordering of tasks in node_list as a node_list

	Parameters:
	------
	node_list : lst
		THe list of tasks to be optimized

============================================================
II. EXAMPLE USAGE:
============================================================
import brute_force as bf
import taskNodeGeneratorUtils
import todoListGenerator as tdlg
from taskNodeGeneratorUtils import recipeLibrary

# create recipeLibrary
rlibs = recipeLibrary('./test_recipes/')

# extract necessary tasks
target = ['Boil Water', 'Pasta']
tlist = rlibs.extract_list(target)

# optimize task ordering
tasklist = bf.maximizer(tlist)

# generate json file
tdlg.tnodelist_tojson(tasklist, out_fname = './example.json')

Author: Yuan Wang
Contact/Support: yuanw@princeton.edu
"""

import taskNodeGeneratorUtils as tnUtils
from taskNodeGeneratorUtils import recipeLibrary
import sys
import itertools

def maximizer(node_list):
	"""
	Description:
	------
	Returns the optimal ordering of tasks in node_list as a node_list

	Parameters:
	------
	node_list : lst
		THe list of tasks to be optimized

	"""
	start_node = node_list[0]
	done_node = node_list[1]

	rg = range(0, len(node_list))
	champ = rg
	best = -1
	optimal_ordering = None
	first_valid_run = True
	# generate permutations from rg

	# iterate through permutations
	permutations = create_iterations(rg, node_list)
	#permutations = itertools.permutations(rg)
	for seq in permutations:
		#seq is a tuple
		seq = tuple(seq)
		#print(seq)

		cost, tlist = evaluate(node_list, seq)

		if cost < 0: continue

		# name first champion
		if (first_valid_run): 
			champ = seq
			first_valid_run = False
			optimal_ordering = tlist
			print("first solution found")
			continue

		# update champion
		if (best > cost):
			champ = seq
			best = cost
			optimal_ordering = tlist

	return optimal_ordering

def create_iterations(rg, node_list):
	# bubble ingredients to top
	head = []
	tail = []
	head.append(0)
	tail.append(1)

	# list of active tasks
	atasks = []

	# list of ingredients
	ingredients = []
	
	for i in range(2, len(node_list)):
		node = node_list[i]
		if isIngredient(node):
			ingredients.append(i)
		else: 
			atasks.append(i)

	head = head + ingredients

	atasks_permutes = itertools.permutations(atasks)
	out_permutes = []

	for seq in atasks_permutes:
		out_permutes.append(head + list(seq) + tail)

	return out_permutes

class smart_premutes:
    def __init__(self, head, mid, tail):
        self.head = head
        self.mid = mid
        self.tail = tail
        self.mids = itertools.permutations(mid)

    def __iter__(self):
        return self

    def next(self):
        return self.mids.next

def isIngredient(node):

	if len(node.depends) == 0: 

		return True
	if len(node.depends) == 1:
		if node.depends[0] == 0: 
			if node.act_time == 0.0:
				return True

	return False


def evaluate(node_list, ordering):
	"""
	computes time to execute ordering
	"""
	current_time = 0.0
	# star_time[i] := start time of task at node_list[i]
	start_time = [-1.0] * (len(node_list) )
	end_time = [-1.0] * (len(node_list) )

	
	end_time[0] = [0.0]

	# must start with 0, must end with done node
	if ordering[0] != 0: return -1, None

	if ordering[len(node_list) - 1] != 1: return -1, None



	for i in ordering:
		node = node_list[i]
		# check that all its dependencies are satisfied
		# i.e. if something isn't started yet, then give up
		for j in node.depends:
			if (start_time[j] < 0): return -1, None

		# simulate wait until task is available; make sure all dependencies have ended
		for dpd in node.depends:
			if end_time[dpd] > current_time:
				current_time = end_time[dpd]

		# we do this, and we increase active time by time required
		start_time[i] = current_time
		end_time[i] = current_time + max(node_list[i].back_time, node_list[i].act_time)
		
		current_time = current_time + node_list[i].act_time

	new_list = []
	# add in start and stop times
	for i in range(len(node_list)):
		node_list[i].beg_time = start_time[i]
		node_list[i].elap_time = end_time[i] - start_time[i]

	node_list = sorted(node_list, key=keyFunc)

	return current_time, node_list

def keyFunc(node):
	return node.beg_time


def main():
	target = ['Boil Water', 'Pasta']
	lib = recipeLibrary('./recipes_basic_yw/')

	node_list = lib.extract_list(target)

	optimal_ordering = maximizer(node_list)
	for node in optimal_ordering:
		print(node.task_str)
	
if __name__ == "__main__":
	main()