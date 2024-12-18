import collections
from typing import Callable

from Bazaar.Common.JSON.CheatingPlayer import CheatNonExistentEquation, CheatBankCannotTrade, CheatBuyUnavailableCard, \
    CheatWalletCannotBuyCard, CheatWalletCannotTrade
from Bazaar.Common.JSON.ExceptionPlayers import ExceptSetupPlayer, ExceptPorTPlayer, ExceptCardsPlayer, ExceptWinPlayer
from Bazaar.Common.JSON.TimeoutPlayer import TimeoutSetupPlayer, TimeoutPorTPlayer, TimeoutCardsPlayer, TimeoutWinPlayer
from Bazaar.Common.cards import Card
from Bazaar.Common.equations import EquationTable, Equation
from Bazaar.Common.game_player import GamePlayer
from Bazaar.Common.JSON.methods import Methods
from Bazaar.Common.pebble_collection import PebbleCollection
from Bazaar.Common.turn_section import TurnSection
from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.mechanism import PlayerMechanism
from Bazaar.Player.player_action import ActionType
from Bazaar.Player.strategy import Strategy, StrategyNode
from Bazaar.Referee.game_state import GameState


class BazaarDeserializer:
    """
    A utility class for deserializing game data into Bazaar game objects.
    """
    def __init__(self):
        self.strategy = None
        self.list_of_equations = []

    @staticmethod
    def m8_entry(actors: list[list[str]], equations: list[tuple[list[str], list[str]]], game: dict) -> (
            tuple)[list[PlayerMechanism], EquationTable, GameState]:
        equation_table = BazaarDeserializer.equations_to_equation_table(equations)
        mechanisms = BazaarDeserializer.actors_to_mechanisms(actors)
        game_state = BazaarDeserializer._state_to_bazaar_game_state(game, equation_table)

        return mechanisms, equation_table, game_state

    @staticmethod
    def m10_entry(equations: list[tuple[list[str], list[str]]], game: dict) -> GameState:
        equation_table = BazaarDeserializer.equations_to_equation_table(equations)
        game_state = BazaarDeserializer._playerless_state_to_bazaar_game_state(game, equation_table)

        return game_state

    @staticmethod
    def _playerless_state_to_bazaar_game_state(game: dict, equation_table: EquationTable) -> GameState:
        bank = BazaarDeserializer.pebble_collection(game["bank"])
        deck = [BazaarDeserializer.card(card) for card in game["cards"]]
        tableau = [BazaarDeserializer.card(card) for card in game["visibles"]]
        players = []

        return GameState(equation_table, deck, tableau, bank, players, 0, TurnSection.START_OF_TURN)

    @staticmethod
    def actors_to_mechanisms(actors: list[list[str]]) -> list[PlayerMechanism]:
        return [BazaarDeserializer._actor_to_mechanism(actor) for actor in actors]

    @staticmethod
    def equations_to_equation_table(equations: list[tuple[list[str], list[str]]]) -> EquationTable:
        return EquationTable(
            [
                BazaarDeserializer.equation(equation)
                for equation in equations
            ]
        )

    @staticmethod
    def _state_to_bazaar_game_state(game: dict, equation_table: EquationTable) -> GameState:
        bank = BazaarDeserializer.pebble_collection(game["bank"])
        deck = [BazaarDeserializer.card(card) for card in game["cards"]]
        tableau = [BazaarDeserializer.card(card) for card in game["visibles"]]
        players = [BazaarDeserializer.game_player(player) for player in game["players"]]

        return GameState(
            equation_table,
            deck,
            tableau,
            bank,
            players,
            0,
            TurnSection.START_OF_TURN,
        )

    @staticmethod
    def json_to_turn_state(turn_state: dict) -> TurnState:
        return TurnState(tableau=[BazaarDeserializer.card(c) for c in turn_state.get("cards")],
                         bank=BazaarDeserializer.pebble_collection(turn_state.get("bank")),
                         scores=[turn_state.get("active").get("score")] + turn_state.get("scores"),
                         player=BazaarDeserializer.game_player(turn_state.get("active")))

    @staticmethod
    def _actor_to_mechanism(actor: list[str]) -> PlayerMechanism:
        """
        Converts an actor representation into a PlayerMechanism instance.
        """
        name = actor[0]
        strategy = BazaarDeserializer._policy_to_strategy(actor[1])

        match len(actor):
            case 2:
                return PlayerMechanism(name, strategy)
            case 3:
                return BazaarDeserializer._bad_actor_to_mechanism(name, strategy, actor[2])
            case 4:
                if actor[2] == "a cheat":
                    return BazaarDeserializer._cheating_actor_to_mechanism(name, strategy, actor[3])
                else:
                    return BazaarDeserializer._mixed_actor_to_mechanism(name, strategy, actor[2], int(actor[3]))

        raise ValueError(f"Invalid actor format: {actor}")

    @staticmethod
    def _bad_actor_to_mechanism(name: str, strategy: Strategy, method: str) -> PlayerMechanism:
        """
        returns a PlayerMechanism that raises an exception when the given method is called
        """
        match method:
            case Methods.SETUP:
                return ExceptSetupPlayer(name, strategy)
            case Methods.REQUEST_P_OR_T:
                return ExceptPorTPlayer(name, strategy)
            case Methods.REQUEST_CARDS:
                return ExceptCardsPlayer(name, strategy)
            case Methods.WIN:
                return ExceptWinPlayer(name, strategy)
            case _:
                raise ValueError(f"Invalid method: {method}")

    @staticmethod
    def _cheating_actor_to_mechanism(name: str, strategy: Strategy, cheat: str) -> PlayerMechanism:
        """
        returns a PlayerMechanism that cheats in the specified manner.
        """
        match cheat:
            case "use-non-existent-equation":
                return CheatNonExistentEquation(name, strategy)
            case "bank-cannot-trade":
                return CheatBankCannotTrade(name, strategy)
            case "wallet-cannot-trade":
                return CheatWalletCannotTrade(name, strategy)
            case "buy-unavailable-card":
                return CheatBuyUnavailableCard(name, strategy)
            case "wallet-cannot-buy-card":
                return CheatWalletCannotBuyCard(name, strategy)
            case _:
                raise ValueError(f"Invalid cheat type: {cheat}")

    @staticmethod
    def _mixed_actor_to_mechanism(name: str, strategy: Strategy, method: str, count: int) -> PlayerMechanism:
        """
        Modifies a PlayerMechanism to include mixed behavior for a specified method.

        This method enhances a `PlayerMechanism` instance by overriding a specified method with
        behavior that runs normally for a given number of turns (`count`) before raising a
        `BazaarException`. It enables dynamic customization of player behavior in the game.
        """
        match method:
            case Methods.SETUP:
                return TimeoutSetupPlayer(name, strategy, count)
            case Methods.REQUEST_P_OR_T:
                return TimeoutPorTPlayer(name, strategy, count)
            case Methods.REQUEST_CARDS:
                return TimeoutCardsPlayer(name, strategy, count)
            case Methods.WIN:
                return TimeoutWinPlayer(name, strategy, count)
            case _:
                raise ValueError(f"Invalid method: {method}")

    @staticmethod
    def _policy_to_strategy(policy: str) -> Strategy:
        policy_map: dict[str, Callable[[StrategyNode], int]] = {
            "purchase-points": lambda node: node.score,
            "purchase-size": lambda node: sum(
                1
                for action in node.actions
                if action.action_type == ActionType.PURCHASE_CARD
            ),
        }

        try:
            value_function = policy_map[policy]
        except KeyError:
            raise ValueError(f"Unknown policy: {policy}")

        return Strategy(equation_search_depth=4, value_function=value_function)

    @staticmethod
    def pebble_collection(pebbles: list[str]) -> PebbleCollection:
        collection = collections.defaultdict(int)
        for color in pebbles:
            collection[color] += 1

        return PebbleCollection(dict(collection))

    @staticmethod
    def equation(equation: tuple[list[str], list[str]]) -> Equation:
        left = BazaarDeserializer.pebble_collection(equation[0])
        right = BazaarDeserializer.pebble_collection(equation[1])

        return Equation(left, right)

    @staticmethod
    def card(card: dict) -> Card:
        return Card(
            cost=BazaarDeserializer.pebble_collection(card["pebbles"]),
            face=card["face?"],
        )

    @staticmethod
    def game_player(player: dict) -> GamePlayer:
        return GamePlayer(
            purchased_cards=[BazaarDeserializer.card(c) for c in player["cards"]],
            pebbles=BazaarDeserializer.pebble_collection(player["wallet"]),
            score=player["score"],
            active=True
        )
