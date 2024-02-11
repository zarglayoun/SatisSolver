from data_processors.parser import parse_recipes, parse_machines

if __name__ == '__main__':
    recipes = parse_recipes("data/recipes.json")
    print(recipes)
    machines = parse_machines("data/machines.json")
    print(machines)