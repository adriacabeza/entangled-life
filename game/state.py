from __future__ import annotations

from collections import defaultdict

from game.info import Info
import copy
import random
import uuid
from typing import Tuple, Optional

from game.constants import (
    MAP_SIZE,
    MAX_ATTEMPTS,
    MAX_FOOD,
    MAX_QUANTITY_OF_FOOD,
    MIN_DISTANCE_FOOD,
    MIN_FOOD,
    MIN_QUANTITY_OF_FOOD,
    MIN_DISTANCE_SPAWN_SQUARED,
)
from game.player.player import Player
from game.utils import (
    Cell,
    CellType,
    Food,
    MushroomUnit,
    Pos,
    MoveCommand,
    BranchCommand,
    is_valid_position,
)


class State:
    def __init__(
        self,
        info: Info,
        players: list[Player],
        seed: Optional[int] = None,
        output_file: str = "output.csv",
    ):
        super().__init__()
        if seed:
            random.seed(seed)
        self.info: Info = info
        self.round: int = 0
        self._players = {player.name: player for player in players}
        self._food: dict[uuid.UUID, Food] = dict()
        self._output_file: str = output_file
        self._output_buffer: list[str] = list()
        self.grid: list[list[Cell]] = [
            [Cell(type=CellType.NORMAL) for _ in range(MAP_SIZE)]
            for _ in range(MAP_SIZE)
        ]

    def populate_board(self):
        self._generate_mushroom_units()
        self.update_mushroom_units_info()
        self._place_food()
        self.info.food = copy.deepcopy(self._food)

    def update_mushroom_units_info(self):
        new_info = dict()
        for player in self._players.values():
            info_per_player = {"positions": [], "score": 0}
            for mushroom_units in player.mushrooms.values():
                info_per_player["positions"].append(mushroom_units.pos)
            info_per_player["score"] += player.score
            new_info[player.name] = info_per_player
        self.info.players = new_info

    def end_game(self):
        self._print_results()
        self._save_game()

    def next(self) -> None:
        """
        Perform the actions to compute the next state for the next round.
        """
        self._output_buffer.append(f"{self.round}")
        commands = list()
        for _, player in self._players.items():
            for c in player.commands_to_perform:
                commands.append(c)

        # Perform the commands using a random order
        random.shuffle(commands)
        for command in commands:
            if isinstance(command, MoveCommand):
                self._move_mushroom_unit(command)
            elif isinstance(command, BranchCommand):
                self._split(command)

        # Update the total score after executing commands
        self._compute_total_score()

        # Place food on the grid
        self._update_food()

        # update information about players
        self.update_mushroom_units_info()

        self._update_round()

    def _compute_total_score(self):
        """
        Compute the total score for each player based on the number of food cells they occupy on the grid.
        """
        for player_name, player in self._players.items():
            for mushroom_unit in player.mushrooms.values():
                new_points = 0
                if (
                    self.grid[mushroom_unit.pos.i][mushroom_unit.pos.j].type
                    == CellType.FOOD
                ):
                    new_points += 1
                player.score += new_points
                self.info.total_score[player_name] = player.score

    def _generate_mushroom_units(self):
        """
        Generate mushroom units for each player.
        """
        for (
            player_name,
            player,
        ) in self._players.items():  # Iterate over players
            self._output_buffer.append(f"Player {player_name} spawn units")
            # Spawn a new mushroom unit with a random ID and position (Pos())
            self._spawn(MushroomUnit(id=uuid.uuid4(), player=player_name, pos=Pos()))

    def _place_food(self):
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
                is_valid = self._food_valid(i, j)
            if is_valid:
                f = Food(
                    id=uuid.uuid4(),
                    quantity=random.randint(MIN_QUANTITY_OF_FOOD, MAX_QUANTITY_OF_FOOD),
                    pos=Pos(i, j),
                )
                self._food[f.id] = f
                cell = Cell(type=CellType.FOOD, food_id=f.id)
                self.grid[i][j] = cell
                self._output_buffer.append(f"Food {f.id} placed in {f.pos}")

    def _food_valid(self, i: int, j: int) -> bool:
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

    def _print_results(self):
        """
        Prints the results and the names of the winning players
        :return:
        """
        max_score = 0
        winners: list[str] = list()
        for player_name, player in self._players.items():
            print(f"Player {player_name} got score {player.score}")
            self._output_buffer.append(f"Player {player_name} got score {player.score}")
            if player.score > max_score:
                max_score = player.score
                winners = [player_name]
            elif player.score == max_score:
                winners.append(player_name)
        for winner in winners:
            print(f"Player {winner} got top score: {max_score}")

    def _split(self, command: BranchCommand):
        mushroom_unit = self._find_mushroom_unit(command.id)
        new = MushroomUnit(
            id=uuid.uuid4(), player=mushroom_unit.player, pos=mushroom_unit.pos
        )
        self._spawn(new)
        self.info.players[mushroom_unit.player]["positions"].append(new.pos)
        self._output_buffer.append(
            f"Mushroom {mushroom_unit.id} splits into two, new mushroom unit:{new.id}"
        )

    def _spawn(self, mushroom_unit: MushroomUnit):
        """
        Decide positions to spawn the mushroom units of each player.
        """
        valid_position = False
        attempts = 0

        while not valid_position and attempts < MAX_ATTEMPTS:
            i, j = self._get_random_spawn_position()
            if self._valid_to_spawn(i, j, mushroom_unit.player):
                valid_position = True
                self.grid[i][j].mushroom_id = mushroom_unit.id
                mushroom_unit.pos = Pos(i, j)
                self._players[mushroom_unit.player].mushrooms[
                    mushroom_unit.id
                ] = mushroom_unit
                self._output_buffer.append(
                    f"Mushroom {mushroom_unit.id} placed in {mushroom_unit.pos}"
                )

        if not valid_position:
            raise RuntimeError("Could not find a cell to start mushroom units")

    def _valid_to_spawn(self, i: int, j: int, player_name: str) -> bool:
        """
        Check that you are not spawning too near to your rival.

        Args:
            i (int): The row index for the potential spawn position.
            j (int): The column index for the potential spawn position.
            player_name (str): The ID of the player trying to spawn.

        Returns:
            bool: True if it is valid to spawn the mushroom unit at the given position, False otherwise.
        """
        for player in self._players.values():
            if player_name != player.name:
                for mushroom_unit in player.mushrooms.values():
                    dist_squared = (i - mushroom_unit.pos.i) ** 2 + (
                        j - mushroom_unit.pos.j
                    ) ** 2
                    if dist_squared < MIN_DISTANCE_SPAWN_SQUARED:
                        return False
        return True

    def _update_round(self):
        self.round += 1
        self.info.round += 1

    def _find_mushroom_unit(self, id: uuid.UUID) -> Optional[MushroomUnit]:
        mushroom_unit = None
        for player in self._players.values():
            mushroom_unit = player.mushrooms.get(id)
            if mushroom_unit is not None:
                break
        return mushroom_unit

    def _move_mushroom_unit(self, command: MoveCommand) -> None:
        """
        Move the mushroom unit of a player based on the command.

        Args:
            command (MoveCommand): The command containing the ID of the mushroom unit and the direction to move.
        """
        mushroom_unit = self._find_mushroom_unit(command.id)
        if mushroom_unit is not None:
            next_pos = mushroom_unit.pos + command.dir
            if is_valid_position(next_pos):
                self._output_buffer.append(
                    f"{mushroom_unit.player},{mushroom_unit.id} from"
                    f" {mushroom_unit.pos} to "
                    f"{next_pos}"
                )
                mushroom_unit.pos = next_pos

    def _save_game(self) -> None:
        with open(self._output_file, "w", newline="") as file:
            for row in self._output_buffer:
                file.write(f"{row}\n")

    def _update_food(self) -> None:
        """
        Update the state of food on the grid based on mushroom units from players.

        If there is any mushroom unit from any player in the same cell position as food, increment the score of the player
        and subtract one from the quantity of food. If the quantity of food becomes zero, remove it from the grid.
        """
        for player_name, player in self._players.items():
            # Check if any player's mushroom unit is at the same position as the food
            for _, mushroom_unit in player.mushrooms.items():
                cell = self.grid[mushroom_unit.pos.i][mushroom_unit.pos.j]
                if cell.food_id and cell.type == CellType.FOOD:
                    player.score += 1
                    self._food[cell.food_id].quantity -= 1

                    # Update information class as well
                    self.info.total_score[player_name] += 1
                    self.info.food[cell.food_id].quantity -= 1

                    if self._food[cell.food_id].quantity == 0:
                        # Remove the food cell from the grid
                        self.grid[mushroom_unit.pos.i][
                            mushroom_unit.pos.j
                        ].type = CellType.NORMAL
                        del self._food[cell.food_id]
                        del self.info.food[cell.food_id]
                        self._output_buffer.append(f"Food {cell.food_id} was finished")

    @staticmethod
    def _get_random_spawn_position() -> Tuple[int, int]:
        """
        Get a random position for mushroom unit spawn.

        Returns:
            Tuple[int, int]: A tuple representing the row and column indices for the spawn position.
        """
        return random.randrange(0, MAP_SIZE - 1), random.randrange(0, MAP_SIZE - 1)
