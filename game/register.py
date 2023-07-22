from __future__ import annotations

from typing import Callable, Union


class Registry:
    # A dictionary to store the registered players and their factory functions
    registered_players: dict[str, Callable[[], "Player"]] = {}

    @classmethod
    def register(cls, name: str, factory: Callable[[], "Player"]) -> None:
        """
        Register a player class with its name and factory function.

        Args:
            name (str): The name to register the player class under.
            factory (Callable[[], Player]): A factory function that creates instances of the player class.
        """
        cls.registered_players[name] = factory

    @classmethod
    def new_player(cls, name: str) -> Union["Player", RuntimeError]:
        """
        Create a new instance of a player class by name.

        Args:
            name (str): The name of the player class to create an instance of.

        Returns:
            Player or None: An instance of the player class if registered, None otherwise.
        """
        if name in cls.registered_players:
            factory = cls.registered_players[name]
            return factory()
        else:
            raise KeyError(f"Player {name} not registered.")

    @staticmethod
    def print_players() -> None:
        """Print the names of all registered player classes."""
        for name in Registry.registered_players:
            print(name)

    @staticmethod
    def register_player(factory: Callable[[], "Player"]) -> None:
        """
        Register a player class using its factory function.

        Args:
            factory (Callable[[], Player]): A factory function that creates instances of the player class.
        """
        # Get the class name as the name for registration
        class_name = factory.__qualname__
        Registry.register(class_name, factory)
