from enum import StrEnum, auto


class TurnSection(StrEnum):
    """Represents the different sections of a player's turn in the Bazaar game:
    START_OF_TURN: Before any action is taken on the player's turn.
    MAKING_EXCHANGES: After an exchange has been made (a pebble cannot be taken, and further equation uses will not
    remove cards from the deck.)
    PURCHASING_CARDS: The player's only remaining valid action is to take cards (a state reached after either a pebble
    was taken, or a card was purchased.)
    """

    START_OF_TURN = auto()
    MAKING_EXCHANGES = auto()
    PURCHASING_CARDS = auto()
