from typing import Callable
from pydantic import BaseModel, PositiveInt
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated
from Bazaar.Common.pebble_collection import PebbleCollection


def has_specific_pebble_count(
    count: PositiveInt,
) -> Callable[[PebbleCollection], PebbleCollection]:
    """
    Creates a validator function to ensure a PebbleCollection has a specific total count of pebbles.

    Parameters:
        count (int): The expected total number of pebbles.

    Returns:
        Callable[[PebbleCollection], PebbleCollection]: A validator function that takes a PebbleCollection
        and returns it if valid, or raises a ValueError if the total pebble count doesn't match the specified count.

    """

    def validator(pebbles: PebbleCollection) -> PebbleCollection:
        """
        A validator to ensure that the sum of all pebbles in the collection is equal to the specified count.

        Parameters:
            pebbles (PebbleCollection): The pebble collection to validate.

        Returns:
            PebbleCollection: The validated pebble collection.

        Raises:
            ValueError: Raised if the number of pebbles is not equal to the specified count.
        """
        if sum(pebbles.values()) != count:
            raise ValueError(f"Sum of pebble numbers was not equal to {count}")
        return pebbles

    return validator


class Card(BaseModel):
    """
    The Card class represents the cards that are purchasable by the players of the Bazaar game.
    Each Card either has a face on it or does not (cards with a face are worth more points on purchase
    than cards without), and has a cost to purchase. The cost of a card must always be exactly five pebbles,
    an invariant which is enforced internally.
    """

    cost: Annotated[PebbleCollection, AfterValidator(has_specific_pebble_count(5))]
    face: bool

    def __init__(self, cost: PebbleCollection, face: bool) -> None:
        """
        Creates a new instance of the Card class.

        Attributes:
            cost (PebbleCollection): The cost to purchase a card.
            face (bool): Whether the card has a smiley face or not.

        Raises:
            ValueError: Raised if the cost of the card is not exactly five pebbles, to preserve the
            invariant.
        """
        super().__init__(cost=cost, face=face)

    def can_acquire(self, pebbles: PebbleCollection) -> bool:
        """
        Returns whether this card can be acquired with the passed in pebbles.

        Arguments:
            pebbles (PebbleCollection): The collection of pebbles to check for acquiring this card.

        Returns:
            True if the card can be acquired with the given pebbles. False otherwise.
        """
        return pebbles >= self.cost

    @property
    def cost(self) -> PebbleCollection:
        return PebbleCollection(self.cost.pebbles)

    @property
    def face(self) -> bool:
        return self.face
