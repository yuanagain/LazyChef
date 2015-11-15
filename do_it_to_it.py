import brute_force as bf
import taskNodeGeneratorUtils
import todoListGenerator as tdlg
from taskNodeGeneratorUtils import recipeLibrary




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

if __name__ == "__main__":
	main2()