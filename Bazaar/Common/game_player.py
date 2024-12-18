from typing import Optional

from pydantic import BaseModel

from Bazaar.Common.cards import Card
from Bazaar.Common.pebble_collection import PebbleCollection, Color


class GamePlayer(BaseModel):
    """Represents the information needed to represent a player in Bazaar, as seen by the referee."""
    wallet: PebbleCollection
    score: int
    active: bool
    purchased_cards: list[Card]

    def __init__(
            self, pebbles: PebbleCollection, score: int, active: bool, purchased_cards: list[Card] = None
    ):
        """
        Initialize a new GamePlayer instance.

        Arguments:
            pebbles (PebbleCollection): The player's current collection of pebbles.
            score (int): The player's current score.
            active (bool): Whether the player is still active in the game.
        """
        super().__init__(wallet=pebbles, score=score, active=active, purchased_cards=purchased_cards)
        if purchased_cards is None:
            self.purchased_cards = list()

    def purchase_card(self, card: Card) -> None:
        """
        update what cards this player has purchased
        """
        self.purchased_cards.append(card)
