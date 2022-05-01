from dataclasses import dataclass


@dataclass
class Tweet:
    id: str
    user: any
    text: str

