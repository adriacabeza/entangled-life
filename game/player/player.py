from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import final
from uuid import UUID

from game.info import Info
from game.utils import Action, MushroomUnit, BranchCommand, Pos


class Player(Action, ABC):
    """
    Abstract base class for defining player behavior in the game.

    This class extends Action, and State classes and should be subclassed by concrete player
    implementations.
    """

    def __init__(self) -> None:
        super().__init__()
        self.info = None
        self.name = self.__class__.__name__
        self.mushrooms: dict[UUID, MushroomUnit] = {}
        self.score: int = 0

    def set_info(self, info: Info):
        self.info = info

    @abstractmethod
    def play(self) -> None:
        """
        Play method, invoked once per each round.
        Subclasses should override this method to define the player's behavior during the game.
        """
        pass

    @staticmethod
    @abstractmethod
    def factory():
        """
        Factory method to create a new instance of the player class.

        Subclasses should implement this method to create a new instance of themselves.

        Returns:
            Player: A new instance of the player class.
        """
        pass

    def reset(self):
        """
        Reset the player state using the provided Info.
        """
        # Clear the previous actions and state data
        super().__init__()

    def winning(self) -> bool:
        """
        Check if the player is winning the game.

        A player is considered winning if their total score is greater than the total score of all other players.

        Returns:
            bool: True if the player is winning, False otherwise.
        """
        for player in self.info.players:
            if player != self.name and self.info.get_score(player.name) <= self.score:
                return False
        return True

    def split(self, mushroom_unit: MushroomUnit) -> bool:
        if (
            self.score > 5
            and len(self.mushrooms) < 50
            and self.commands_tried < self.MAX_COMMANDS
        ):
            self.execute(BranchCommand(mushroom_unit.id))
            self.score -= 5
            self.info.players[mushroom_unit.player]["score"] -= 5
            return True
        else:
            return False
