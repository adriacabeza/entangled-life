import uuid

import pytest

from game.player.player import Player
from game.info import Info
from game.utils import Dir, MushroomUnit, Pos, MoveCommand


class DummyPlayer(Player):
    def play(self) -> None:
        pass

    @staticmethod
    def factory():
        return DummyPlayer()


@pytest.fixture
def player():
    return DummyPlayer()


def test_player_initial_info(player):
    assert player.info is None
    assert player.name == "DummyPlayer"
    assert player.mushrooms == {}
    assert player.score == 0


def test_set_info(player):
    info = Info()
    player.set_info(info)
    assert player.info == info


def test_reset(player):
    mushroom = MushroomUnit(id=uuid.uuid4(), player="dummy", pos=Pos(1, 1))
    # add a command to commands to perform
    player.execute(MoveCommand(mushroom.id, Dir.EAST))
    assert player.commands_to_perform == [MoveCommand(mushroom.id, Dir.EAST)]
    assert player.commands_tried == 1

    player.reset()
    assert player.commands_to_perform == []
    assert player.commands_tried == 0


def test_winning(player):
    info = Info()
    player.set_info(info)

    # Add some scores to the info
    info._total_score = {"DummyPlayer": 10, "Player1": 15, "Player2": 5}

    assert not player.winning()

    # Increase DummyPlayer's score to be the highest
    info._total_score["DummyPlayer"] = 20

    assert player.winning()
