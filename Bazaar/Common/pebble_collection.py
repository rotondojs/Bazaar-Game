from enum import Enum
from typing import Self

from pydantic import BaseModel, Field, PositiveInt

from Bazaar.Common.exceptions import BazaarException


class Color(Enum):
    """
    An enumeration representing the colors which a pebble can be in the Bazaar game.
    """

    RED = "red"
    WHITE = "white"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"

    def __str__(self) -> str:
        return self.name


class PebbleCollection(BaseModel):
    """
    The PebbleCollection class represents a collection of pebbles of the defined Colors.
    """

    pebbles: dict[Color, PositiveInt] = Field(default_factory=dict)

    def __init__(self, pebbles: dict[Color, PositiveInt]) -> None:
        """
        Creates a new instance of the PebbleCollection class.

        Attributes:
            pebbles (dict[Color, PositiveInt]): The collection of pebbles to store.
        """
        super().__init__(pebbles=pebbles)

    def __getitem__(self, key: Color) -> PositiveInt:
        """
        Returns the number of pebbles for the passed in Color.

        Defaults to 0 if the Color key is present.

        Arguments:
            key (Color): The color of the pebble to retrieve.

        Returns:
        """
        out = self.pebbles.get(key)
        if out:
            return out
        elif isinstance(key, Color):
            return 0
        raise BazaarException(f'Invalid key: {key}')

    def __setitem__(self, key: Color, value: PositiveInt) -> None:
        """
        Sets the count of pebbles in this PebbleCollection.

        Arguments:
            key (Color): The Color to set.
            value (PositiveInt): The updated count to set.
        """
        if isinstance(key, Color):
            if value == 0:
                self.pebbles.pop(key, None)
            else:
                self.pebbles[key] = value
        else:
            raise BazaarException(f"Pebble collection does not support this key {key}.")

    def __add__(self, other: "PebbleCollection") -> "PebbleCollection":
        """
        Adds the passed in PebbleCollection to this PebbleCollection by adding up individual
        counts of pebbles for each color.

        Arguments:
            other (PebbleCollection): The PebbleCollection to add to this PebbleCollection

        Returns:
            A new PebbleCollection instance with the summed up pebble values.
        """
        new_pebbles = PebbleCollection({})
        for color in Color:
            new_pebbles[color] = self[color] + other[color]
        return new_pebbles

    def __sub__(self, other: Self) -> Self:
        """
        Subtracts the passed in PebbleCollection from this PebbleCollection by subtracting
        individual counts of pebbles for each color.

        Arguments:
            other (PebbleCollection): The PebbleCollection to subtract from this PebbleCollection.

        Returns:
            A new PebbleCollection instance with the difference of pebbles counts.
        """
        new_pebbles = PebbleCollection({})
        for color in Color:
            value = self[color] - other[color]
            if value < 0:
                raise ValueError(
                    f"Tried to subtract {other[color]} {color} pebbles, but only had {self[color]}"
                )
            new_pebbles[color] = value
        return new_pebbles

    def __hash__(self):
        return hash(self.pebbles)

    def __eq__(self, other: Self) -> bool:
        """
        Returns whether two PebbleCollections are equal.

        Arguments:
            other (PebbleCollection): The PebbleCollection to compare with this PebbleCollection.

        Returns:
            True if the two PebbleCollections are equal (same count for each color), False otherwise.
        """
        return all(self[color] == other[color] for color in Color)

    def __ge__(self, other: Self) -> bool:
        """
        Returns whether this PebbleCollection is greater than or equal to the passed
        in PebbleCollection. The comparison of counts is done for each color.

        Arguments:
            other (PebbleCollection): The PebbleCollection to compare with this PebbleCollection.

        Returns:
            True if this PebbleCollection is greater than or equal to the passed in PebbleCollection,
            False otherwise.
        """
        return all(self[color] >= other[color] for color in Color)

    def __le__(self, other: "PebbleCollection") -> bool:
        """
        Returns whether this PebbleCollection is less than or equal to the passed in PebbleCollection.
        The comparison of counts is done for each color.

        Arguments:
            other (PebbleCollection): The PebbleCollection to compare with this PebbleCollection.

        Returns:
            True if this PebbleCollection is less than or equal to the passed in PebbleCollection,
            False otherwise.
        """
        return all(self[color] <= other[color] for color in Color)

    def __repr__(self) -> str:
        pebble_strs = [
            f"{color.value}: {count}" for color, count in self.pebbles.items()
        ]
        return f"PebbleCollection({', '.join(pebble_strs)})"

    def values(self) -> list[PositiveInt]:
        """
        Returns the list of the counts of pebbles for each color in this PebbleCollection, without reference
        to which color is which (the same as dict.values()).

        Returns:
            A list with the counts of all the pebbles for each color in this PebbleCollection.
        """
        return list(self.pebbles.values())

    def as_list_of_colors(self) -> list[Color]:
        """
        Returns this collection as a list of individual pebbles. For example, a
        collection of 2 red and 2 blue would become ["red", "red", "blue", "blue"].

        Returns:
            A list with each pebble in this PebbleCollection.
        """
        list_of_colors = []

        for color in Color:
            for _ in range(self[color]):
                list_of_colors.append(color)

        return list_of_colors

    def items(self) -> list[tuple[Color, PositiveInt]]:
        """
        Returns the list of the counts of pebbles for each color in this PebbleCollection, without reference
        to which color is which (the same as dict.items()).

        Returns:
            A list with the counts of all the pebbles for each color in this PebbleCollection.
        """
        return list(self.pebbles.items())
    
    def __copy__(self) -> Self:
        return PebbleCollection(self.pebbles.copy())
