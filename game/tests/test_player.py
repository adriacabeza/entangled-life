import uuid
from abc import abstractmethod

import pytest

from game.player.player import Player
from game.state import State
from game.utils import Command, Dir, MushroomUnit, Pos


class DummyPlayer(Player):
    def play(self) -> None:
        pass

    @staticmethod
    def factory():
        return DummyPlayer()


@pytest.fixture
def player():
    return DummyPlayer()


def test_player_initial_state(player):
    assert player.state is None
    assert player.name == "DummyPlayer"
    assert player.mushrooms == {}
    assert player.score == 0


def test_set_state(player):
    state = State()
    player.set_state(state)
    assert player.state == state


def test_reset(player):
    mushroom = MushroomUnit(id=uuid.uuid4(), player="dummy", pos=Pos(1, 1))
    # add a command to commands to perform
    player.execute(Command(mushroom.id, Dir.EAST))
    assert player.commands_to_perform == [Command(mushroom.id, Dir.EAST)]
    assert player.commands_tried == 1

    player.reset()
    assert player.commands_to_perform == []
    assert player.commands_tried == 0


def test_winning(player):
    state = State()
    player.set_state(state)

    # Add some scores to the state
    state.total_score = {"DummyPlayer": 10, "Player1": 15, "Player2": 5}

    assert not player.winning()

    # Increase DummyPlayer's score to be the highest
    state.total_score["DummyPlayer"] = 20

    assert player.winning()


def test_split(player):
    state = State()
    state.players = {player.name: player}
    player.set_state(state)

    player.score = 10

    mushroom_unit = MushroomUnit(id=uuid.uuid4(), player="dummy", pos=(2, 2))
    player.mushrooms[mushroom_unit.id] = mushroom_unit
    state.grid[2][2].mushroom_id = mushroom_unit.id
    state.mushrooms[mushroom_unit.id] = mushroom_unit

    assert len(player.mushrooms) == 1
    player.split(mushroom_unit)
    assert len(player.mushrooms) == 2
