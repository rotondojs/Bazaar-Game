**TO:** Matthias Felleisen, Ben Lerner

**FROM:** Rishi Kanabar, Ethan Saff

**DATE:** September 29, 2024

**SUBJECT:** Player Interface Design for the Bazaar Game

For the player interface in the Bazaar game, we propose the following architecture, which allows for a flexible player implementation that handles the variety of possible actions at each point in the player's turn:

```python
class PlayerAction:
    "Represents an individual player action in the Bazaar game, both the type of action and any details necessary to execute the action."
    action_type: str # one of "get_pebble", "use_equation", "purchase_card", "end_turn"
    index: int # -1 if command_type is "get_pebble" or "end_turn", otherwise the index of card to purchase or equation to use
    left_to_right: bool # False if command_type is anything other than "use_equation", otherwise True if the equation should be used left-to-right, False otherwise

# Defined by each player implementation:
def get_player_action(turn_state: TurnState) -> PlayerAction:
    """
    Decides on the next action in the Bazaar game by responding to the given TurnState with a PlayerAction indicating the player's next move. Called by the referee when this player is the current player, at which point the referee executes the given action, and if it is still the player's turn, calls this method again with the new TurnState.
    Note that since TurnState is a complete representation of the game state as visible to the given player, it provides all context necessary for the player to decide on their action. Furthermore, providing the turn state with each command prevents any issues where the player's understanding of the game state and the referee's understanding desync.
    """
    ...
```

As an example of how this code and the GameState implementation written in this milestone allows for a simple and easily understandable high-level code structure, we provide the following sketched implementation of the main game loop, as it would be defined by the referee implementation (note that this is a simplified design, and omits many features that an actual referee implementation would likely wish to include):

```python
def main_loop():
    while True:
        turn_state = self.game_state.get_repr_for_current_player()
        player_action = ai.get_player_action(turn_state)
        try:
            execute_player_action(player_action)
        except BazaarException:
            print("Invalid command attempted!")
            self.game_state.kick_player(self.game_state._current_player_index)
        except GameOver:
            print("Game over!")
            break


def execute_player_action(player_action: PlayerAction):
    match player_action.action_type:
        case "get_pebble":
            self.game_state.get_pebble()
        case "use_equation":
            self.game_state.use_equation(player_action.index, player_action.left_to_right)
        case "purchase_card":
            self.game_state.purchase_card(player_action.index)
        case "end_turn":
            self.game_state.end_turn()
```
