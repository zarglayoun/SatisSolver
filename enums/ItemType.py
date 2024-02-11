from enum import Enum, auto


class ItemType(Enum):
    iron_ore = auto()
    iron_ingot = auto()
    iron_plate = auto()
    iron_rod = auto()
    screw = auto()
    reinforced_iron_plate = auto()
    copper_ore = auto()
    copper_ingot = auto()
    wire = auto()
    cable = auto()
    limestone = auto()
    concrete = auto()
    wood = auto()
    biomass = auto()
    leaves = auto()
    alien_protein = auto()
    solid_biofuel = auto()
    flower_petals = auto()
    copper_sheet = auto()
    rotor = auto()
    modular_frame = auto()
    smart_plating = auto()
    hatcher_remains = auto()
    hog_remains = auto()
    alien_dna_capsule = auto()
    color_cartridge = auto()

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'
