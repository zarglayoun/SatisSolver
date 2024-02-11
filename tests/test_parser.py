import os

from data_processors.parser import parse_recipes, parse_machines
from enums.ItemType import ItemType
from enums.MachineType import MachineType
from models.Machine import Machine
from models.Recipe import Recipe


class TestParser:
    def test_should_return_all_recipes_deserialized_correctly(self):
        # Act
        path = os.path.join(os.path.dirname(__file__), 'data/recipes.json')
        recipes: list[Recipe] = parse_recipes(path)

        # Assert
        assert len(recipes) == 1
        assert recipes[0].inputs[0].item == ItemType.iron_ore
        assert recipes[0].inputs[0].quantity == 1
        assert recipes[0].outputs[0].item == ItemType.iron_ingot
        assert recipes[0].outputs[0].quantity == 1
        assert recipes[0].produced_in[0].machine_type == MachineType.smelter
        assert recipes[0].produced_in[0].cycle_time == 2

    def test_should_return_all_machines_deserialized_correctly(self):
        # Act
        path = os.path.join(os.path.dirname(__file__), 'data/machines.json')
        machines: list[Machine] = parse_machines(path)

        # Assert
        assert machines[0].machine_type == MachineType.smelter
        assert machines[0].energy_consumption == 4
        assert machines[0].built_with[0].item == ItemType.iron_rod
        assert machines[0].built_with[0].quantity == 5
        assert machines[0].built_with[1].item == ItemType.wire
        assert machines[0].built_with[1].quantity == 8
