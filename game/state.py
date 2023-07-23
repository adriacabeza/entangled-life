from __future__ import annotations

import csv
import random
import uuid
from typing import Optional, Tuple

from game.constants import (
    MAP_SIZE,
    MAX_ATTEMPTS,
    MAX_FOOD,
    MAX_QUANTITY_OF_FOOD,
    MIN_DISTANCE_FOOD,
    MIN_DISTANCE_SPAWN_SQUARED,
    MIN_FOOD,
    MIN_QUANTITY_OF_FOOD,
)
from game.utils import Cell, CellType, Command, Food, MushroomUnit, Pos


class State:
    def __init__(self, output_file: str = "output.csv", seed: Optional[int] = None):
        self.round: int = 0
        self.players = dict()
        self.grid: list[list[Cell]] = [
            [Cell(type=CellType.NORMAL) for _ in range(MAP_SIZE)]
            for _ in range(MAP_SIZE)
        ]
        self.total_score: dict[str, int] = dict()
        self.food: dict[uuid.UUID, Food] = dict()
        self.mushrooms: dict[uuid.UUID, MushroomUnit] = dict()
        self.output_file: str = output_file
        self.output_buffer: list[str] = list()
        if seed:
            random.seed(seed)
        else:
            random.seed(69)

    def compute_total_score(self):
        """
        Compute the total score for each player based on the number of food cells they occupy on the grid.
        """
        for player_name, player in self.players.items():
            for mushroom_unit in player.mushrooms.values():
                new_points = 0
                if (
                    self.grid[mushroom_unit.pos.i][mushroom_unit.pos.j].type
                    == CellType.FOOD
                ):
                    new_points += 1
                player.score += new_points
                self.total_score[player_name] = player.score

    def generate_mushroom_units(self):
        """
        Generate mushroom units for each player.
        """
        for (
            player_name,
            player,
        ) in self.players.items():  # Iterate over players
            self.output_buffer.append(f"Player {player_name} spawn units")
            # Spawn a new mushroom unit with a random ID and position (Pos())
            self.spawn(MushroomUnit(id=uuid.uuid4(), player=player_name, pos=Pos()))

    def place_food(self):
        """
        Place food randomly on the grid.
        """
        number_of_food = random.randrange(MIN_FOOD, MAX_FOOD)
        for k in range(number_of_food):
            is_valid = False
            n_attempt = 0
            i, j = -1, -1
            while n_attempt < MAX_ATTEMPTS and not is_valid:
                i = random.randrange(0, MAP_SIZE - 1)
                j = random.randrange(0, MAP_SIZE - 1)
                is_valid = self.food_valid(i, j)
            if is_valid:
                f = Food(
                    id=uuid.uuid4(),
                    quantity=random.randint(MIN_QUANTITY_OF_FOOD, MAX_QUANTITY_OF_FOOD),
                    pos=Pos(i, j),
                )
                self.food[f.id] = f
                self.grid[i][j] = Cell(type=CellType.FOOD, food_id=f.id)
                self.output_buffer.append(f"Food {f.id} placed in {f.pos}")

    def food_valid(self, i: int, j: int) -> bool:
        """
        Check if the given position is valid for placing food.

        Args:
            i (int): The row index of the position.
            j (int): The column index of the position.

        Returns:
            bool: True if the position is valid, False otherwise.
        """
        for ii in range(
            max(0, i - MIN_DISTANCE_FOOD),
            min(MAP_SIZE, i + MIN_DISTANCE_FOOD - 1),
        ):
            for jj in range(
                max(0, j - MIN_DISTANCE_FOOD),
                min(MAP_SIZE, j + MIN_DISTANCE_FOOD - 1),
            ):
                # Check if the cell contains a mushroom unit or food
                if (
                    self.grid[ii][jj].mushroom_id is not None
                    or self.grid[ii][jj].type == CellType.FOOD
                ):
                    return False
        return True

    def print_results(self):
        """
        Prints the results and the names of the winning players
        :return:
        """
        max_score = 0
        winners: list[str] = list()
        for player_name, player in self.players.items():
            print(f"Player {player_name} got score {player.score}")
            self.output_buffer.append(f"Player {player_name} got score {player.score}")
            if player.score > max_score:
                max_score = player.score
                winners.append(player_name)
            elif player.score == max_score:
                winners.append(player_name)
        for winner in winners:
            print(f"Player {winner} got top score: {max_score}")

    def next(self) -> None:
        """
        Perform the actions to compute the next state for the next round.
        """
        self.output_buffer.append(f"{self.round}")
        commands = list()
        for _, player in self.players.items():
            for c in player.commands_to_perform:
                commands.append(c)

        # Perform the commands using a random order
        random.shuffle(commands)
        for command in commands:
            self.move_mushroom_unit(command)

        # Update the total score after executing commands
        self.compute_total_score()

        # Place food on the grid
        self.update_food()

        # Increment the round counter
        self.round += 1

    def move_mushroom_unit(self, command: Command) -> None:
        """
        Move the mushroom unit of a player based on the command.

        Args:
            command (Command): The command containing the ID of the mushroom unit and the direction to move.
        """
        mushroom_unit = next(
            (mu for mu in self.mushrooms.values() if mu.id == command.id), None
        )
        if mushroom_unit is not None:
            next_pos = mushroom_unit.pos + command.dir
            if self.is_valid_position(next_pos):
                self.output_buffer.append(
                    f"{mushroom_unit.player},{mushroom_unit.id} from"
                    f" {mushroom_unit.pos} to "
                    f"{next_pos}"
                )
                mushroom_unit.pos = next_pos

    def save_game(self) -> None:
        with open(self.output_file, "w", newline="") as file:
            for row in self.output_buffer:
                file.write(f"{row}\n")

    def update_food(self) -> None:
        """
        Update the state of food on the grid based on mushroom units from players.

        If there is any mushroom unit from any player in the same cell position as food, increment the score of the player
        and subtract one from the quantity of food. If the quantity of food becomes zero, remove it from the grid.
        """
        for player_name, player in self.players.items():
            # Check if any player's mushroom unit is at the same position as the food
            for _, mushroom_unit in player.mushrooms.items():
                cell = self.grid[mushroom_unit.pos.i][mushroom_unit.pos.j]
                if cell.food_id and cell.type == CellType.FOOD:
                    player.score += 1
                    self.total_score[player_name] += 1
                    self.food[cell.food_id].quantity -= 1
                    if self.food[cell.food_id].quantity == 0:
                        # Remove the food cell from the grid
                        self.grid[mushroom_unit.pos.i][mushroom_unit.pos.j] = Cell(
                            type=CellType.NORMAL
                        )
                        del self.food[cell.food_id]
                        self.output_buffer.append(f"Food {cell.food_id} was finished")

    def spawn(self, mushroom_unit: MushroomUnit):
        """
        Decide positions to spawn the mushroom units of each player.
        """
        valid_position = False
        attempts = 0

        while not valid_position and attempts < MAX_ATTEMPTS:
            i, j = self._get_random_spawn_position()
            if self.valid_to_spawn(i, j, mushroom_unit.player):
                valid_position = True
                self.grid[i][j].mushroom_id = mushroom_unit.id
                self.mushrooms[mushroom_unit.id] = mushroom_unit
                mushroom_unit.pos = Pos(i, j)
                self.players[mushroom_unit.player].mushrooms[
                    mushroom_unit.id
                ] = mushroom_unit
                self.output_buffer.append(
                    f"Mushroom {mushroom_unit.id} placed in {mushroom_unit.pos}"
                )

        if not valid_position:
            raise RuntimeError("Could not find a cell to start mushroom units")

    def valid_to_spawn(self, i: int, j: int, player_name: str) -> bool:
        """
        Check that you are not spawning too near to your rival.

        Args:
            i (int): The row index for the potential spawn position.
            j (int): The column index for the potential spawn position.
            player_name (str): The ID of the player trying to spawn.

        Returns:
            bool: True if it is valid to spawn the mushroom unit at the given position, False otherwise.
        """
        for player in self.players.values():
            if player_name != player.name:
                for mushroom_unit in player.mushrooms.values():
                    dist_squared = (i - mushroom_unit.pos.i) ** 2 + (
                        j - mushroom_unit.pos.j
                    ) ** 2
                    if dist_squared < MIN_DISTANCE_SPAWN_SQUARED:
                        return False
        return True

    @staticmethod
    def _get_random_spawn_position() -> Tuple[int, int]:
        """
        Get a random position for mushroom unit spawn.

        Returns:
            Tuple[int, int]: A tuple representing the row and column indices for the spawn position.
        """
        return random.randrange(0, MAP_SIZE - 1), random.randrange(0, MAP_SIZE - 1)

    @staticmethod
    def is_valid_position(pos: Pos) -> bool:
        return 0 <= pos.i < MAP_SIZE and 0 <= pos.j < MAP_SIZE
