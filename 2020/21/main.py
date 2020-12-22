import sys

def make_choices(lines):
    all_ingredients = set()
    choices = {}  # map allergens to potential foods
    for line in lines:
        parts = line.rstrip(')').split(' (contains ')
        ingredients = set(parts[0].split())
        allergens = parts[1].split(', ')
        all_ingredients |= ingredients

        for allergen in allergens:
            if allergen not in choices:
                choices[allergen] = ingredients.copy()
            else:
                choices[allergen] &= ingredients.copy()
    return (choices, all_ingredients)

def identify_foods(choices):
    identified = {}
    while len(identified) < len(choices):
        ingredient = None
        for allergen, ingredients in choices.items():
            if len(ingredients) == 1:
                ingredient = ingredients.pop()
                break
        identified[allergen] = ingredient
        # Remove this ingredient from other choices
        for ingredients in choices.values():
            ingredients.discard(ingredient)
    return identified


with open(sys.argv[1]) as f:
    data = f.read()

# Part 1
choices, all_ingredients = make_choices(data.splitlines())
possible_allergens = set()
for _,ingredients in choices.items():
    possible_allergens |= ingredients
safe_foods = all_ingredients - possible_allergens
part1 = sum([data.count(ingredient) for ingredient in safe_foods])
print(f'Part 1: {part1}')

# Part 2
identified = identify_foods(choices)
sorted_allergens = sorted(list(identified.keys()))
dangerous = [identified[a] for a in sorted_allergens]
print(f'Part 2: {",".join(dangerous)}')
