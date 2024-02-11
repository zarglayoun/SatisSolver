from dataclasses import dataclass, field
from typing import List
from enums.MachineType import MachineType
from models.Ingredient import Ingredient


@dataclass
class Machine:
    machine_type: MachineType
    energy_consumption: int
    built_with: List[Ingredient]
