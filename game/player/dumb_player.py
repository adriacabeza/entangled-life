from __future__ import annotations

import random
from typing import Optional

from game.player.player import Player
from game.utils import Command, Dir, MushroomUnit


class DumbPlayer(Player):
    """
    A simple implementation of the Player class for test purposes.

    This DumbPlayer moves mushrooms randomly within the board.
    """

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def factory() -> DumbPlayer:
        """
        Factory: returns a new instance of this class.

        Returns:
            DumbPlayer: A new instance of the DumbPlayer player class.
        """
        return DumbPlayer()

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
        for _, mushroom in self.mushrooms.items():
            self.move(mushroom)
