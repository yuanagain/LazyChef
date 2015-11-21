'''
recipeValidator.py
By: Hector Solis
for - Princeton Fall 2015 Hackathon

func - clearPath(name, path_list): Recursive helper function no need to call
            -Checks if there is a clear path in the dependencies
                Prints a warning if one or more recipes are messed up
func - validateRecipe(): validates a recipe in the "recipe_files" directory
                        also returns a list of end nodes of the involved recipes
        Example:
            validateRecipe() -> ['Juicer', 'Cherry', 'Trail Mix', 'Cook Pasta', 'Piggy Wiggy', 'Bake Brownies']
            validateRecipe() {invalid recipe} -> One or more files is messed up. Check ~
func - validateRecipeWithPath(filepath): validates a recipe in a given driectory
        Example:
            validateRecipeWithPath("recipes_main") -> ['Baked Potato', 'Macaroni Baking']
'''

import os


def clearPath(name, path_list):
    my_dependencies = path_list[name]
    if len(my_dependencies) == 0:
        return
    for d in my_dependencies:
        if d in path_list:
            clearPath(d, path_list)
        else:
            print("One or more files is messed up. Check " + d)
            return


def validateRecipe():
    list_of_tasks = os.listdir("recipe_files")
    my_dir = 'recipe_files\\'
    task_list = {}
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
            task_list[name] = dependencies_list
        f.closed
        dependencies_list = []
    print(task_list)
    list_end_nodes = []
    for my_name in task_list:
        is_end_node = True
        for other_name in task_list:
            if my_name != other_name:
                dependencies = task_list[other_name]
                # If other dictionary pair has dependencies check to see if something depends on those dependencies
                if len(dependencies) != 0:
                    for d in dependencies:
                        if my_name == d:
                            # what it depends on is in list so valid
                            is_end_node = False
                            break
        if is_end_node:
            list_end_nodes.append(my_name)
    print(list_end_nodes)
    for end_node in list_end_nodes:
        clearPath(end_node, task_list)
    return list_end_nodes

def validateRecipeWithPath(filepath):
    list_of_tasks = os.listdir(filepath)
    my_dir = filepath + '\\'
    task_list = {}
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
            task_list[name] = dependencies_list
        f.closed
        dependencies_list = []
    print(task_list)
    list_end_nodes = []
    for my_name in task_list:
        is_end_node = True
        for other_name in task_list:
            if my_name != other_name:
                dependencies = task_list[other_name]
                # If other dictionary pair has dependencies check to see if something depends on those dependencies
                if len(dependencies) != 0:
                    for d in dependencies:
                        if my_name == d:
                            # what it depends on is in list so valid
                            is_end_node = False
                            break
        if is_end_node:
            list_end_nodes.append(my_name)
    print(list_end_nodes)
    for end_node in list_end_nodes:
        clearPath(end_node, task_list)
    return list_end_nodes
