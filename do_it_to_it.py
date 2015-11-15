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
from do_it_to_it import KRAKEN
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


class KRAKEN:
	def __init__(self, recipe_src = './test_recipes/'):
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
	fg = KRAKEN("./recipes_demo/")
	tg = ['Bake Potatoes', 'Potatoes']
	print(fg.produce_dict(tg))

if __name__ == "__main__":
	main()