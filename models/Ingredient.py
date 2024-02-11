from dataclasses import dataclass
from enums.ItemType import ItemType


@dataclass
class Ingredient:
    item: ItemType
    quantity: int
