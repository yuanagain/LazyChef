"""
task_dict['name']
task_dict['active']
task_dict['start_time']
task_dict['end_time']
task_dict['time_delta']
task_dict['descripton']

"""

import sys
import json

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


	task_dict['name'] = task_name
	task_dict['active'] = False
	task_dict['start_time'] = time_array
	task_dict['end_time'] = dependencies
	task_dict['descripton'] = description
	return task_dict

def json_dump(task_list):
	dump_data = json.dumps(task_dict)
	return dump_data

def generate_todo_list(tnode_list):
	"""
	Parameters
	------
	tnode_list : TaskNode[]
		A list of TaskNodes
	------
	Turns a list of nodes into a list of 
	"""

	task_list = []
	current_time = 0.0

	for tnode in tnode_list:
		createTask(tnode, current_time)
	return task_list


def main():
	

	dump_data = json_dump(task_dict)
	print dump_data

	tn = TaskNode()




if __name__ == "__main__":
	main()