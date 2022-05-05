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
    ingredients: str


@dataclass
class Equipment:
    name: str
    grade: str
    image: str
    description: str

