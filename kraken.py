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
class KRAKEN():

Description:
Allows user to generate task orderings
============================================================
II. USEFUL METHODS
============================================================
    
__init__(self, recipe_src = './test_recipes/'):
    Description:
    ------
    Creates a KRAKEN object
    
    Parameters
    ------
    def_list_dir : fname (default =  ./recipe_files/')
        A list of recipe defintions


produce_dict(self, target):

	Description:
	------
	Returns dict of tasks corresponding to target

	Parameters:
	------
	target : list
		A list of recipes we desire to complete

============================================================
III. EXAMPLE USAGE:
============================================================
from kraken import KRAKEN
fg = KRAKEN()
tg = ['Boil Water', 'Pasta']
print(fg.produce_dict(tg))

Author: Yuan Wang
Contact/Support: yuanw@princeton.edu
"""

import brute_force as bf
import taskNodeGeneratorUtils
import todoListGenerator as tdlg
from taskNodeGeneratorUtils import recipeLibrary
from galgo import GraphAlgo
import time


class KRAKEN:
	def __init__(self, recipe_src = './recipe_files/'):
		self.rlibs = recipeLibrary(recipe_src)


	def produce_json(self, target, json_fname = './example_01.json'):
		"""

		"""
		tlist = self.rlibs.extract_list(target)
		tasklist = bf.maximizer(tlist)
		tdlg.tnodelist_tojson(tasklist, out_fname = json_fname)

	def produce_dict(self, target):
		"""
		Description:
		------
		Returns dict of tasks corresponding to target

		Parameters:
		------
		target : list
			A list of recipes we desire to complete
		"""
		tlist = self.rlibs.extract_list(target)
		tasklist = bf.maximizer(tlist)
		return tdlg.tnodelist_todict(tasklist)

	def get_ingredients(self, target):
		"""
		Description:
		-------
		Get ingredients required for the target

		Parameters:
		-------
		target : list
			A list of recipes we desire to find ingredients for
		"""
		tlist = self.rlibs.extract_list(target)
		return taskNodeGeneratorUtils.get_ingredients(tlist)

	def produce_dict_graph(self, target):
		"""
		Description:
		------
		Returns dict of tasks corresponding to target

		Parameters:
		------
		target : list
			A list of recipes we desire to complete
		"""
		tlist = self.rlibs.extract_list(target)
		galgo = GraphAlgo(tlist)
		tasklist = galgo.optimizeRecipe()

		return tdlg.tnodelist_todict(tasklist)


def main2():
	# create recipeLibrary
	rlibs = recipeLibrary('./test_recipes/')

	# extract necessary tasks
	target = ['Boil Water', 'Pasta']
	tlist = rlibs.extract_list(target)

	# optimize task ordering
	tasklist = bf.maximizer(tlist)

	# generate json file
	tdlg.tnodelist_tojson(tasklist, out_fname = './example.json')

def main():
	'''
	start_time_yuan = time.clock()
	fg = KRAKEN("./recipes_basic_yw/")
	tg = ['Baked Potato', 'Bake Pasta and Cheese']
	#tg = ['Bake Blondie']
	print(fg.produce_dict(tg))
	end_time_yuan = time.clock()
	print(end_time_yuan - start_time_yuan)
	'''
	start_time_ilya = time.clock()
	fg = KRAKEN("./recipes_main/canapes/")
	#tg = ['Bake Potatoes', 'Bake Pasta and Cheese']
	tg = ['Put Cranberries']
	#tg = ['Bake Brownies']
	#tg = ['Baked Potato', 'Bake Pasta and Cheese']
	#       'Bake Potatoes', 'Boiling Water', \
	#       'Boil Water', 'Cheese', 'Cook Pasta', \
	#       'Macaroni Baking', 'Mix Cheese In', \
	#       'Oven Heated', 'Pasta', 'Potatoes', \
	#       'Potato Baking', 'Preheat Oven', 'Water']
	print(fg.produce_dict_graph(tg))
	end_time_ilya = time.clock()
	print(end_time_ilya - start_time_ilya)
	
	'''
	fg = KRAKEN('./more_recipes/')
	tg = ['Piggy Wiggy', 'Cocktail Sausages', 'Roll Dough',\
           'Wrap Sausages', 'Turn on Oven', 'Preheat Oven']
	print(fg.produce_dict_graph(tg))
	'''

	'''
	fg = KRAKEN('./test_recipes/')
	tg = ['add_salt','boil_water','dice_tomatoes',\
	          'drain_pasta','pasta_in_water','pot_on_stove',\
	          'prepare_drink','tomatoes_on_pasta']
	print(fg.produce_dict_graph(tg))
	'''

if __name__ == "__main__":
	main()