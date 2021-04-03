import util

ingredients_file = 'input_files/day_21.txt'


def check_allergens():
    recipy_list = util.parse_file_as_list(ingredients_file)
    ingredients_allergens_dict = [{ingredients: allergens for ingredients, allergens in recipy.split('(')} for recipy in recipy_list]

    print(ingredients_allergens_dict)


check_allergens()
