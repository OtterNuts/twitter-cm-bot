from dataclasses import dataclass


@dataclass
class Monster:
    name: str
    grade: str
    image: str
    description: str
    recipe: str

