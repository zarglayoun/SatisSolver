from dataclasses import dataclass, field
from typing import List
from models.Ingredient import Ingredient
from models.ProductionMethod import ProductionMethod


@dataclass
class Recipe:
    inputs: List[Ingredient]
    outputs: List[Ingredient]
    produced_in: List[ProductionMethod]
