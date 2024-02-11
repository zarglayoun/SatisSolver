from enum import Enum, auto


class MachineType(Enum):
    smelter = auto()
    constructor = auto()
    assembler = auto()
    biomass_burner = auto()
    power_pole = auto()
    power_line = auto()

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'
