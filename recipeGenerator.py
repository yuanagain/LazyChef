import sys
import json




def createTask(task_name, time_array, dependencies, description):
	task_dict = dict()
	task_dict['task_name'] = task_name
	task_dict['time_array'] = time_array
	task_dict['dependencies'] = dependencies
	task_dict['descripton'] = description
	return task_dict

def json_dump(task_dict):
	dump_data = json.dumps(task_dict)
	print(dump_data)

def main():
	print("Enter Task Name")
	task_name = sys.stdin.readline()
	
	print("Enter completion Time, format: <hours>,<seconds>,<minutes>")
	time_array = [int(el) for el in sys.stdin.readline().split()]
	
	print("Enter Dependencies, comma separated:")
	dependencies = sys.stdin.readline().split(',')
	if dependencies[0] == "na":
		dependencies = []
	
	print("Enter a detailed task description:")
	description = sys.stdin.readline()

	task_dict = createTask(task_name, time_array, dependencies, description)

	json_dump(task_dict)



if __name__ == "__main__":
	main()