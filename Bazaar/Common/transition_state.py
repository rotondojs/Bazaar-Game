from pydantic import BaseModel, NonNegativeInt

from Bazaar.Common.cards import Card
from Bazaar.Common.pebble_collection import PebbleCollection
from Bazaar.Common.turn_section import TurnSection


class TransitionState(BaseModel):
    """
    Represents the resulting state after a player's action in the Bazaar game.
    """

    pebbles: PebbleCollection
    bank: PebbleCollection
    score: NonNegativeInt
    tableau: list[Card]
    burn_cards: NonNegativeInt
    turn_section: TurnSection
