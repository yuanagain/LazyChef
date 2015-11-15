import brute_force as bf
import taskNodeGeneratorUtils
import todoListGenerator as tdlg
from taskNodeGeneratorUtils import recipeLibrary


class fileGen:
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
		returns dict of tasks corresponding to target
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
	fg = fileGen()
	tg = ['Boil Water', 'Pasta']
	print(fg.produce_dict(tg))

if __name__ == "__main__":
	main()