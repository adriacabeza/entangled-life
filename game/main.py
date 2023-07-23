import importlib
import inspect
import pkgutil
import time
from pprint import pprint

import game.player as player
from game.constants import NUMBER_OF_ROUNDS
from game.player.player import Player
from game.register import Registry
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

    # Create the game state
    game_state = State()
    game_state.players = {player.name: player for player in players}
    for player in players:
        player.set_state(game_state)

    # Generate initial mushroom units for the players
    game_state.generate_mushroom_units()
    game_state.place_food()

    # Run the fight for a fixed number of rounds
    start = time.time()
    for round_number in range(NUMBER_OF_ROUNDS):
        for player in players:
            player.reset()
            player.play()
        # Perform the actions for the next round
        game_state.next()

        # Print the current state after each round
    game_state.print_results()
    print(f"time elapsed {time.time()-start}")
    game_state.save_game()


if __name__ == "__main__":
    # Discover and register all player subclasses using the Registry
    run()
