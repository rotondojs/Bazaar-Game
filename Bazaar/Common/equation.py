from typing import Annotated

from pydantic import AfterValidator, BaseModel, PositiveInt

from Bazaar.Common.pebble_collection import PebbleCollection


def _validate_equation(
        equation: "Equation",
        pebble_lower_bound: PositiveInt = 1,
        pebble_upper_bound: PositiveInt = 4,
) -> bool:
    """
    A validator to ensure that both sides of the passed in equation are valid.
        - Total number of pebbles on each side must be between the lower and upper bound inclusive.
        - Both sides should not have the same color of pebbles.

    Parameters:
        equation (Equation): The equation to validate.
        pebble_lower_bound (PositiveInt): Smallest number of pebbles an equation side can contain.
        pebble_upper_bound (PositiveInt): Largest number of pebbles an equation side can contain.

    Returns:
        True if the collection passes the validation criteria, False otherwise.
    """
    left, right = equation.left, equation.right

    for side, name in [(left, "Left"), (right, "Right")]:
        total_pebbles = sum(side.values())
        if not (pebble_lower_bound <= total_pebbles <= pebble_upper_bound):
            return False

    left_colors = set([i[0] for i in left.items()])
    right_colors = set([i[0] for i in right.items()])
    overlap = left_colors.intersection(right_colors)
    return not overlap


class _EquationInternal(BaseModel):
    """
    An internal implementation class to hold the left and right side of the pebble equation.
    """

    left: PebbleCollection
    right: PebbleCollection


class Equation(BaseModel):
    """
    The Equation class represents an equation in the game of Bazaar. Each side of the equation
    has a pebbles that can be interchanged for pebbles on the other side of the equation. Each
    side must have between 1 and 4 (inclusive) pebbles and two sides may not have a pebble color in common,
    an invariant which is enforced internally.
    """
    root: Annotated[_EquationInternal, AfterValidator(_validate_equation)]
    _left: PebbleCollection
    _right: PebbleCollection

    def __init__(self, left: PebbleCollection, right: PebbleCollection) -> None:
        """
        Creates a new instance of the Equation class.

        Attributes:
            left (PebbleCollection): The left side of the equation.
            right (PebbleCollection): The right side of the equation.
        """
        super().__init__(root=_EquationInternal(left=left, right=right))
        self._left = left
        self._right = right

    def __repr__(self):
        return f"Equation(left={self._left}, right={self._right})"

    def __hash__(self):
        if self.left < self.right:
            return hash(frozenset((self.left, self.right)))
        return hash(frozenset((self.right, self.left)))

    def __eq__(self, other: "Equation") -> bool:
        """
        Check if two equations are equal.

        Returns:
            True if the two equations are equal, False otherwise.
        """
        return (
                (self.left == other.left
                 and self.right == other.right)
                or (self.left == other.right
                    and self.right == other.left)
        )

    @property
    def left(self) -> PebbleCollection:
        """The left side of the equation."""
        return self._left.model_copy()

    @property
    def right(self) -> PebbleCollection:
        """The right side of the equation."""
        return self._right.model_copy()

    def is_usable(self, pebbles: PebbleCollection) -> bool:
        """
        Returns whether this equation can be applied to the passed in PebbleCollection.

        Arguments:
            pebbles (PebbleCollection): The PebbleCollection to test with this equation.

        Returns:
            True if this equation can be applied to the passed in PebbleCollection, False otherwise.
        """
        return pebbles >= self.left or pebbles >= self.right

    def is_usable_in_direction(
            self, pebbles: PebbleCollection, bank: PebbleCollection, right_to_left: bool
    ) -> bool:
        """
        Returns whether this equation can be applied to the passed in PebbleCollection in the specified direction.

        Arguments:
            pebbles (PebbleCollection): The wallet to test with this equation.
            bank (PebbleCollection): The bank to test with this equation.
            right_to_left (bool): Whether to test the equation from right to left.

        Returns:
            bool: True if this equation can be applied to the passed in PebbleCollection in the specified direction
        """
        if right_to_left:
            return pebbles >= self.right and bank >= self.left
        return pebbles >= self.left and bank >= self.right

    def __str__(self):
        return str(self.left) + str(self.right)
