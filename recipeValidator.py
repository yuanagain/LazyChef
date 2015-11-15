import os

list_of_tasks = os.listdir("recipe_files")
my_dir = 'recipe_files\\'
task_list = []
dependencies_list = []
for current_task in list_of_tasks:
    with open(my_dir + current_task, 'r') as f:
        name = f.readline()
        if name.endswith('\n'):
            name = name[:-1]
        f.readline()
        f.readline()
        f.readline()
        tear = f.readline()
        while tear != "": # first while loop code
            if tear.endswith('\n'):
                tear = tear[:-1]
            dependencies_list.append(tear)
            tear = f.readline()
        task_list.append({name:dependencies_list})
    f.closed
    dependencies_list = []
print(task_list)
list_end_nodes = []
for pair in task_list:
    my_name = list(pair.keys())[0]
    print("name: " + my_name)
    is_end_node = True
    for temp in task_list:
        other_name = list(temp.keys())[0]
        if my_name != other_name:
            dependencies = temp[other_name]
            # If other dictionary pair has dependencies check to see if something depends on those dependencies
            if len(dependencies) != 0:
                for d in dependencies:
                    if my_name == d:
                        # what it depends on is in list so valid
                        print(d + " : I'm about to break")
                        is_end_node = False
                        break
    if is_end_node:
        list_end_nodes.append(my_name)
print("Here come the end nodes")
print(list_end_nodes)


