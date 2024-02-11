from dataclasses import dataclass
from enums.MachineType import MachineType


@dataclass
class ProductionMethod:
    machine_type: MachineType
    cycle_time: int
