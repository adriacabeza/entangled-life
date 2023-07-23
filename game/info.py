from __future__ import annotations

import uuid
from typing import Union

from game.constants import (
    MAP_SIZE,
)
from game.utils import Cell, Pos, Food


class Info:
    """
    Class containing information that will be available from the point of view of the player, this will be updated
    from the state at each round but will not have any impact on the game itself (this is done in order to avoid
    cheaters).
    """

    def __init__(self):
        self.players: dict[str, dict[str, Union[int, list[Pos]]]] = dict()
        self.round: int = 0
        self.food: dict[uuid.UUID, Food] = dict()
        self.total_score: dict[str, int] = dict()

    def get_score(self, player_name: str) -> int:
        return self.total_score[player_name]
