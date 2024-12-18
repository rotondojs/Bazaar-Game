from pydantic import BaseModel

from Bazaar.Referee.game_state import GameState


class IObserver(BaseModel):
    """
    Interface for a game observer handling game states and game over events.
    """
    async def receive_state(self, game_state: GameState):
        """
        pass a game state to an observer.
        """

    async def game_over(self):
        """
        inform an observer that a game is over.
        """
