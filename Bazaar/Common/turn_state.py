from pydantic import BaseModel

from Bazaar.Common.cards import Card
from Bazaar.Common.game_player import GamePlayer
from Bazaar.Common.pebble_collection import PebbleCollection


class TurnState(BaseModel):
    """
    Represents the state of a turn in the Bazaar game.

    This class encapsulates all the information needed to represent the current state
    of the game from a specific player's perspective.
    """
    tableau: list[Card]
    bank: PebbleCollection
    scores: list[int]
    player: GamePlayer

    def __init__(
        self,
        tableau: list[Card],
        bank: PebbleCollection,
        scores: list[int],
        player: GamePlayer
    ):
        """
        Initialize a new TurnState instance.

        Arguments:
            tableau (list[Card]): The list of cards available for purchase.
            bank (PebbleCollection): The current state of the bank's pebbles.
            scores (list[NonNegativeInt]): List of the other players scores in turn order
            player (GamePlayer): The game player whose turn is being represented.
        """
        super().__init__(
            tableau=tableau,
            bank=bank,
            scores=scores,
            player=player
        )
