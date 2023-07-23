from __future__ import annotations

import random
from typing import Optional

from game.player.player import Player
from game.utils import Dir, MushroomUnit, Command


class DumbPlayer2(Player):
    """
    Another Dumb Player to make it fight against DumbPlayer 1 for test purposes
    """

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def factory() -> DumbPlayer2:
        """
        Factory: returns a new instance of this class.

        Returns:
            DumbPlayer: A new instance of the DumbPlayer player class.
        """
        return DumbPlayer2()

    def move(self, mushroom: Optional[MushroomUnit]) -> None:

        """
        Move a mushroom with the given identifier id.

        Args:
            mushroom (MushroomUnit): Mushroom to move.

        Moves the mushroom in a random direction, if the new position is valid.
        """
        if mushroom:
            pos = mushroom.pos
            # Try to move to a position within the board with a random direction.
            direction = random.choice(list(Dir))
            next_pos = pos + direction
            if self.state.is_valid_position(next_pos):
                self.execute(Command(mushroom.id, direction))

    def play(self) -> None:
        """
        Play method, invoked once per each round.

        Move each mushroom owned by this player.
        """
        mushrooms = list(self.mushrooms.values())
        for mushroom in mushrooms:
            self.move(mushroom)
            if self.score > 5:
                self.split(mushroom)
