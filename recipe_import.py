import sys
import json


def 

def main():

	recipe_files = sys.stdin.readlines()

	for recipe_fname in recipe_files:
		json.load(recipe_fname)




if __name__ == "__main__":
	main()