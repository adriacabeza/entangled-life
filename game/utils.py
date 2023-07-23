from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Set, Union
from uuid import UUID


class Dir(Enum):
    """
    Enumeration of different directions with their corresponding (i, j) offsets.
    """

    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)
    NORTHEAST = (1, -1)
    NORTHWEST = (-1, -1)
    SOUTHEAST = (1, 1)
    SOUTHWEST = (-1, 1)


@dataclass
class Pos:
    """
    Represents a position on the board with (i, j) coordinates.
    """

    i: int = 0
    j: int = 0

    def __iadd__(self, other: Union[Dir, Pos]) -> Pos:
        """
        Perform in-place addition of the given direction or position.

        Args:
            other (Union[Dir, Pos]): The direction or position to add.

        Returns:
            Pos: The resulting position after the addition.
        """
        if isinstance(other, Dir):
            self.i += other.value[0]
            self.j += other.value[1]
        elif isinstance(other, Pos):
            self.i += other.i
            self.j += other.j
        return self

    def __add__(self, other: Union[Dir, Pos]) -> Pos:
        """
        Add the given direction or position to the current position.

        Args:
            other (Union[Dir, Pos]): The direction or position to add.

        Returns:
            Pos: The resulting position after the addition.
        """
        if isinstance(other, Dir):
            return Pos(self.i + other.value[0], self.j + other.value[1])
        elif isinstance(other, Pos):
            return Pos(self.i + other.i, self.j + other.j)

    def __eq__(self, other):
        """
        Check if two positions are equal.

        Args:
            other: The other position to compare with.

        Returns:
            bool: True if positions are equal, False otherwise.
        """
        return self.i == other.i and self.j == other.j

    def __str__(self):
        """
        Get a string representation of the position.

        Returns:
            str: The string representation of the position.
        """
        return f"({self.i}, {self.j})"


class CellType(Enum):
    """
    Enumeration of different cell types.
    """

    FOOD = auto()
    NORMAL = auto()


@dataclass
class Cell:
    """
    Represents a cell on the game board with its attributes.
    """

    mushroom_id: Union[UUID, None] = None
    food_id: Union[UUID, None] = None
    type: CellType = CellType.NORMAL


@dataclass
class MushroomUnit:
    """
    Represents a mushroom unit with its attributes.
    """

    id: UUID  # The unique id for this mushroom during the game.
    player: str  # The player that owns this mushroom.
    pos: Pos  # The position on the board.


@dataclass
class Food:
    """
    Represents food with its attributes.
    """

    id: UUID  # The unique id for this food during the game.
    quantity: int  # Quantity of food. This means that at least #quantity rounds are needed to finish this resource
    pos: Pos  # The position on the board.


@dataclass
class Command:
    """
    Represents a command with the ID of the mushroom unit and a direction.
    """

    id: UUID
    dir: Dir


class Action:
    """
    Stores the commands requested by a player in a round.
    """

    MAX_COMMANDS: int = 100

    def __init__(self):
        """
        Initialize Action with an empty list of commands, an empty set of
        mushroom units that have already performed a command, and a counter for commands tried.
        """
        self.commands_tried: int = 0
        self.mushrooms_with_commands: Set[UUID] = set()
        self.commands_to_perform: List[Command] = []

    def execute(self, command: Command):
        """
        Execute a command and add it to the list of commands to perform in this round.

        Args:
            command (Command): The command to be executed.

        Raises:
            RuntimeError: If the maximum number of commands is exceeded.
        """
        if self.commands_tried == self.MAX_COMMANDS:
            raise RuntimeError("Too many commands were asked in a round")
        self.commands_tried += 1
        self.commands_to_perform.append(command)
        self.mushrooms_with_commands.add(command.id)
