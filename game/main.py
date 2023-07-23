import importlib
import inspect
import pkgutil
import time
from pprint import pprint

import game.player as player
from game.constants import NUMBER_OF_ROUNDS
from game.player.player import Player
from game.register import Registry
from game.info import Info
from game.state import State


def discover_player_classes():
    """
    Automatically discover and register all player classes in the player.py file.
    """
    for module_info in pkgutil.iter_modules(
        path=player.__path__, prefix=player.__name__ + "."
    ):
        module = importlib.import_module(module_info.name)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, Player) and obj != Player:
                # Register the player class if it is a subclass of Player
                Registry.register_player(obj)


def run():
    # Discover and register all player subclasses
    # Get the list of registered player names from the Registry
    # Automatically discover and register all player classes
    discover_player_classes()
    registered_players = list(Registry.registered_players.keys())
    # Create players using the registered names
    players = [Registry.new_player(name) for name in registered_players]

    # Create game information available for each player
    info = Info()
    for player in players:
        player.set_info(info)

    # Create the game state
    state = State(info, players)

    # Generate initial mushroom units for the players
    state.populate_board()

    # Run the fight for a fixed number of rounds
    start = time.time()
    for round_number in range(NUMBER_OF_ROUNDS):
        for player in players:
            player.reset()
            player.play()
        # Perform the actions for the next round
        state.next()

        # Print the current state after each round
    state.end_game()
    print(f"time elapsed {time.time()-start}")


if __name__ == "__main__":
    # Discover and register all player subclasses using the Registry
    run()
