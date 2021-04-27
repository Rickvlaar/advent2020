import util

ingredients_file = 'input_files/day_21.txt'
test_file = 'input_files/day_21_test.txt'


def check_allergens():
    recipy_list = util.parse_file_as_list(ingredients_file)

    ingredients_allergens_split = [recipy.split(' (contains ') for recipy in recipy_list]
    allergens_ingredients_sets = [[set(row[1].replace(')', '').split(', ')), set(row[0].split(' '))] for row in ingredients_allergens_split]

    # map allergen to each set it is named in
    allergen_ingredients_dict = {}
    all_ingredients_set = set()
    combined_recipe_list = []
    for allergen_set, ingredient_set in allergens_ingredients_sets:
        for allergen in allergen_set:
            if allergen not in allergen_ingredients_dict:
                allergen_ingredients_dict[allergen] = []
            allergen_ingredients_dict[allergen].append(ingredient_set)
        all_ingredients_set |= ingredient_set
        combined_recipe_list.extend(list(ingredient_set))

    # check which allergens intersect only on one ingredient in their sets
    determined_allergen_ingredient_dict = {}
    all_allergens_set = set(allergen_ingredients_dict.keys())
    while len(all_allergens_set) > 0:
        for allergen, recipes in allergen_ingredients_dict.items():
            # skip ingredients already found
            if allergen not in determined_allergen_ingredient_dict:
                # remove found allergens from intersection
                intersection = set.intersection(*recipes).difference(set(determined_allergen_ingredient_dict.values()))

                if len(intersection) == 1:
                    determined_allergen_ingredient_dict[allergen] = intersection.pop()
                    all_allergens_set.remove(allergen)

    # count occurrences of non-allergen ingredients
    safe_ingredients_set = all_ingredients_set.difference(set(determined_allergen_ingredient_dict.values()))
    ingredient_counts = [combined_recipe_list.count(ingredient) for ingredient in safe_ingredients_set]

    print(determined_allergen_ingredient_dict)
    print(sum(ingredient_counts))

    danger_list = list(determined_allergen_ingredient_dict.keys())
    danger_list.sort()
    poison_string = ''
    for danger in danger_list:
        poison_string += determined_allergen_ingredient_dict.get(danger) + ','
    print(poison_string)


check_allergens()
