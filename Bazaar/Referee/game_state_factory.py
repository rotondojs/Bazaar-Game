import collections
import random

from pydantic import BaseModel, Field, NonNegativeInt
from Bazaar.Common.cards import Card
from Bazaar.Common.equations import Equation, EquationTable
from Bazaar.Common.game_player import GamePlayer
from Bazaar.Common.pebble_collection import PebbleCollection, Color
from Bazaar.Common.turn_section import TurnSection
from Bazaar.Referee.game_state import GameState


class GameStateFactory(BaseModel):
    """
    A factory class for creating GameState instances with customizable parameters.
    """

    seed: NonNegativeInt = Field(default_factory=lambda: random.randint(0, 2 ** 32 - 1))
    visible_card_count: NonNegativeInt = 4
    deck_card_count: NonNegativeInt = 16
    total_bank_pebbles: NonNegativeInt = 100
    card_pebble_count: NonNegativeInt = 5
    num_equations: NonNegativeInt = 10
    equation_lower_bound: NonNegativeInt = 1
    equation_upper_bound: NonNegativeInt = 4
    player_count: NonNegativeInt = 4

    def create(self) -> GameState:
        """
        Create and return a new GameState instance with generated components.

        Returns:
            GameState: A new GameState instance.
        """
        random.seed(self.seed)

        return GameState(
            equation_table=self._generate_equation_table(self.num_equations),
            deck=self._generate_cards(self.deck_card_count),
            tableau=self._generate_cards(self.visible_card_count),
            bank=self._generate_bank(self.total_bank_pebbles),
            players=self._generate_players(self.player_count),
            current_player_index=0,
            turn_section=TurnSection.START_OF_TURN,
        )

    @staticmethod
    def _generate_players(player_count: NonNegativeInt) -> list[GamePlayer]:
        """
        Generate a list of GamePlayer instances.

        Arguments:
            player_count (NonNegativeInt): The number of players to generate.

        Returns:
            list[GamePlayer]: A list of generated GamePlayer instances.
        """
        return [
            GamePlayer(PebbleCollection({}), 0, True, [])
            for _ in range(player_count)
        ]

    def _generate_cards(self, card_count: NonNegativeInt) -> list[Card]:
        """
        Generate a list of Card instances.

        Arguments:
            card_count (NonNegativeInt): The number of cards to generate.

        Returns:
            list[Card]: A list of generated Card instances.
        """
        return [self._generate_card() for _ in range(card_count)]

    @staticmethod
    def _generate_bank(total_bank_pebbles: NonNegativeInt) -> PebbleCollection:
        """
        Generate a PebbleCollection representing the bank.

        Arguments:
            total_bank_pebbles (NonNegativeInt): The total number of pebbles in the bank.

        Returns:
            PebbleCollection: A PebbleCollection instance representing the bank.
        """
        pebbles = collections.defaultdict(int)
        color_count = len(Color)

        for color in Color:
            pebbles[color] = total_bank_pebbles // color_count

        return PebbleCollection(dict(pebbles))

    def _generate_card(self) -> Card:
        """
        Generate a single Card instance.

        Returns:
            Card: A generated Card instance.
        """
        colors = collections.defaultdict(int)

        for _ in range(self.card_pebble_count):
            colors[random.choice(list(Color))] += 1
        face = random.choice([True, False])

        return Card(PebbleCollection(dict(colors)), face)

    def _generate_equation_table(self, num_equations: NonNegativeInt) -> EquationTable:
        """
        Generate an EquationTable with a specified number of equations.

        Arguments:
            num_equations (NonNegativeInt): The number of equations to generate.

        Returns:
            EquationTable: An EquationTable instance with generated equations.
        """
        existing_equations = []
        while len(existing_equations) < num_equations:
            new_equation = self._generate_equation(existing_equations)
            existing_equations.append(new_equation)
        return EquationTable(existing_equations)

    def _generate_equation(self, existing_equations: list[Equation]) -> Equation:
        """
        Generate a single Equation instance that is unique from existing equations.

        Arguments:
            existing_equations (list[Equation]): A list of existing equations to avoid duplicates.

        Returns:
            Equation: A newly generated Equation instance.
        """
        while True:
            left_colors, right_colors = self._select_colors()
            left_pebbles = self._generate_pebbles(left_colors)
            right_pebbles = self._generate_pebbles(right_colors)
            new_equation = Equation(
                PebbleCollection(dict(left_pebbles)),
                PebbleCollection(dict(right_pebbles)),
            )

            if not new_equation.root:
                raise Exception("_generate_equation incorrectly generates equations")

            if new_equation not in existing_equations:
                return new_equation

    @staticmethod
    def _select_colors() -> tuple[list[str], list[str]]:
        """
        Select colors for the left and right sides of an equation.

        Returns:
            tuple[list[str], list[str]]: Two lists of colors for the left and right sides.
        """
        left_colors = random.sample(list(Color), k=2)
        right_colors = random.sample(
            [c for c in Color if c not in left_colors], k=2
        )
        return left_colors, right_colors

    def _generate_pebbles(self, colors: list[str]) -> collections.defaultdict:
        """
        Generate a collection of pebbles for an equation side.

        Arguments:
            colors (list[str]): The colors to choose from when generating pebbles.

        Returns:
            collections.defaultdict: A defaultdict representing the generated pebbles.
        """
        pebbles = collections.defaultdict(int)
        for _ in range(
            random.randint(self.equation_lower_bound, self.equation_upper_bound)
        ):
            pebbles[random.choice(colors)] += 1
        return pebbles
