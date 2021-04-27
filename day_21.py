import util

ingredients_file = 'input_files/day_21.txt'
test_file = 'input_files/day_21_test.txt'


def check_allergens():
    recipy_list = util.parse_file_as_list(test_file)

    ingredients_allergens_split = [recipy.split(' (contains ') for recipy in recipy_list]
    ingredients_allergens_lists = [[row[0].split(' '), row[1].replace(')', '').split(',')] for row in ingredients_allergens_split]

    ingredient_allergens_dict = dict()
    all_ingredients_set = set()
    for ingredients, allergens in ingredients_allergens_lists:
        all_ingredients_set.update(ingredients)
        for allergen in allergens:
            if allergen not in ingredient_allergens_dict:
                ingredient_allergens_dict[allergen] = set(ingredients)
            else:
                ingredient_allergens_dict[allergen].intersection_update(set(ingredients))

    print(all_ingredients_set)
    for ingredient in all_ingredients_set:
        for allergen, ingredients in ingredient_allergens_dict.items():
            if len(ingredients) > 1 and ingredient in ingredients:
                ingredients.remove(ingredient)

    print(ingredient_allergens_dict)


check_allergens()
