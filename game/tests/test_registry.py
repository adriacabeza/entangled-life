import pytest

from game.player.player import Player
from game.register import Registry


@pytest.fixture
def registry_with_dummy_player():
    def create_dummy_player():
        return Player()

    Registry.register("DummyPlayer", create_dummy_player)
    return Registry


def test_register_and_new_player(registry_with_dummy_player):
    registry = registry_with_dummy_player
    player = registry.new_player("DummyPlayer")
    assert isinstance(player, Player)


def test_register_nonexistent_player():
    with pytest.raises(KeyError):
        Registry.new_player("NonExistentPlayer")


def test_register_and_print_players(registry_with_dummy_player, capsys):
    registry = registry_with_dummy_player
    expected_output = "DummyPlayer\n"

    registry.print_players()

    captured = capsys.readouterr()
    assert captured.out == expected_output


def test_register_player_decorator(registry_with_dummy_player):
    @Registry.register_player
    def create_player_three():
        return Player()

    @Registry.register_player
    def create_player_four():
        return Player()

    assert "create_player_three" in Registry.registered_players
    assert "create_player_four" in Registry.registered_players
