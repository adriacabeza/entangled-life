from __future__ import annotations

from game.player.player import Player


class PlayerTemplate(Player):
    """
    A template class for creating new player implementations.

    You should override the play method to define the player's behavior during the game.
    """

    @staticmethod
    def factory() -> PlayerTemplate:
        """
        Factory: returns a new instance of this class.

        Returns:
            PlayerTemplate: A new instance of the PlayerTemplate player class.
        """
        return PlayerTemplate()

    # Types and attributes for your player can be defined here
    # Note: Add any necessary attributes or class-level constants here

    def play(self) -> None:
        """
        Play method, invoked once per each round.

        Subclasses should override this method to define the player's behavior during the game.
        """
        pass
