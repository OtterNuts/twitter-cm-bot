from dataclasses import dataclass


@dataclass
class Monster:
    name: str
    grade: str
    image: str
    description: str
    recipe: str


@dataclass
class Cooking:
    name: str
    description: str
    ingredient: str