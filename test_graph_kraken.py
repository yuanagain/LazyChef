from kraken import KRAKEN


def main():
	fg = KRAKEN("./recipes_basic_yw/")
	tg = ['Bake Potatoes', 'Bake Pasta and Cheese']
	print(fg.produce_dict_graph(tg))


if __name__ == "__main__":
	main()