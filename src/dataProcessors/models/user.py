from dataclasses import dataclass


@dataclass
class User:
    id: str
    닉네임: str
    크리스탈: int
    스테미나: int
    떡밥: int
    B급장비개수: int
    C급장비개수: int
    골드: int
