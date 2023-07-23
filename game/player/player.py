from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from uuid import UUID
from typing import final

from game.state import State
from game.utils import MushroomUnit, Action


class Player(Action, ABC):
    """
    Abstract base class for defining player behavior in the game.

    This class extends Action, and State classes and should be subclassed by concrete player
    implementations.
    """

    def __init__(self) -> None:
        super().__init__()
        self.state = None
        self.name = self.__class__.__name__
        self.mushrooms: dict[UUID, MushroomUnit] = {}
        self.score: int = 0

    def set_state(self, state: State):
        self.state = state

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
        for name, score in self.state.total_score.items():
            if name != self.name and self.state.total_score[self.name] <= score:
                return False
        return True

    @final
    def split(self, mushroom_unit: MushroomUnit) -> bool:
        if self.score > 5 and len(self.mushrooms) < 50:
            self.score -= 5
            new = MushroomUnit(id=uuid.uuid4(), player=self.name, pos=mushroom_unit.pos)
            self.state.spawn(new)
            self.state.output_buffer.append(
                f"Mushroom {mushroom_unit.id} splits into two, new mushroom unit:{new.id}"
            )
            return True
        else:
            return False
