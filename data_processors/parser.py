import json
from typing import Union

from enums.ItemType import ItemType
from enums.MachineType import MachineType
from models.Ingredient import Ingredient
from models.Machine import Machine
from models.Recipe import Recipe
from models.ProductionMethod import ProductionMethod


def parse_recipes(path: str) -> list[Recipe]:
    def create_recipe(recipe_data: dict) -> Recipe:
        return Recipe(
            inputs=[Ingredient(item=ItemType[ing['item']], quantity=ing['quantity']) for ing in recipe_data['inputs']],
            outputs=[Ingredient(item=ItemType[ing['item']], quantity=ing['quantity']) for ing in
                     recipe_data['outputs']],
            produced_in=[
                ProductionMethod(machine_type=MachineType[prod['machine_type']], cycle_time=prod['cycle_time'])
                for prod in recipe_data['produced_in']
            ]
        )

    return _parse_file(path, create_recipe)


def parse_machines(path: str) -> list[Machine]:
    def create_machine(machine_data: dict) -> Machine:
        return Machine(
            machine_type=MachineType[machine_data["machine_type"]],
            energy_consumption=machine_data["energy_consumption"],
            built_with=[
                Ingredient(item=ItemType[ing["item"]], quantity=ing["quantity"]) for ing in machine_data["built_with"]
            ],
        )

    return _parse_file(path, create_machine)


def _parse_file(path: str, create_object_func: [dict, Union[Recipe, Machine]]) -> list[Union[Recipe, Machine]]:
    try:
        with open(path, "r") as file:
            data = json.load(file)
            objects = [create_object_func(obj_data) for obj_data in data]
            return objects
    except Exception:
        print(f"Parser of type {type(create_object_func)} failed to parse the file at {path}")
        raise
