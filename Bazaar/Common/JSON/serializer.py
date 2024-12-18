import json

from Bazaar.Common.cards import Card
from Bazaar.Common.equations import Equation, EquationTable
from Bazaar.Common.game_player import GamePlayer
from Bazaar.Common.pebble_collection import PebbleCollection
from Bazaar.Common.turn_state import TurnState
from Bazaar.Referee.game_state import GameState


class BazaarSerializer:
    """
    A utility class for serializing Bazaar game objects into JSON-compatible formats.
    """
    @staticmethod
    def game_state_to_json(game_state: GameState) -> str:
        return json.dumps(BazaarSerializer.game_state(game_state))

    @staticmethod
    def game_state(game_state: GameState) -> dict:
        # noinspection SpellCheckingInspection
        return {"bank": BazaarSerializer.pebbles(game_state.bank),
                "visibles": BazaarSerializer.cards(game_state.tableau),
                "cards": BazaarSerializer.cards(game_state.deck),
                "players": BazaarSerializer.game_players(game_state.players)}

    @staticmethod
    def turn_state(turn: TurnState) -> dict:
        return {"bank": BazaarSerializer.pebbles(turn.bank),
                "cards": BazaarSerializer.cards(turn.tableau),
                "active": {"wallet": BazaarSerializer.pebbles(turn.wallet), "score": turn.scores[0]},
                "scores": turn.scores}

    @staticmethod
    def game_players(players: list[GamePlayer]) -> list[dict]:
        return [BazaarSerializer.game_player(player) for player in players]

    @staticmethod
    def game_player(player: GamePlayer) -> dict:
        return {"cards": BazaarSerializer.cards(player.purchased_cards),
                "wallet": BazaarSerializer.pebbles(player.wallet),
                "score": player.score}

    @staticmethod
    def cards(cards: list[Card]) -> list[dict]:
        return [BazaarSerializer.card(card) for card in cards]

    @staticmethod
    def card(card: Card) -> dict:
        return {"pebbles": BazaarSerializer.pebbles(card.cost), "face?": card.face}

    @staticmethod
    def equations(equations: EquationTable) -> list[list[list[str]]]:
        return [BazaarSerializer.equation(equation) for equation in equations.get_equations()]

    @staticmethod
    def equation(equation: Equation) -> list[list[str]]:
        return [BazaarSerializer.pebbles(equation.left), BazaarSerializer.pebbles(equation.right)]

    @staticmethod
    def pebbles(pebbles: PebbleCollection) -> list[str]:
        return [pebble.name for pebble in pebbles.as_list_of_colors()]
