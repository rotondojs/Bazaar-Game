**TO:** Matthias Felleisen, Ben Lerner

**FROM:** Rishi Kanabar, Ethan Saff

**DATE:** September 24, 2024

**SUBJECT:** Game State Plan for the Bazaar Game

We propose the following design, to represent the game state available to the referee to adjucate a game.

**Data Representation**

The referee holds an instance of the `GameState` class. The `GameState` class holds all information the referee has concerning the game state, and contains a method which converts this `GameState` into a more limited dictionary which can be sent to players via JSON, containing only the information known by that player. While the referee is responsible for the flow of the overall game, the `GameState` class exposes helper methods to perform the basic operations given by the game rules. The `GameState` class has the following properties:

- A `table` field, which is an `EquationTable` object representing the available equations for trading.

- A `deck` field, which is a list of `Card` objects, representing the purchaseable cards in the deck.

- A `tableau` field, which is a list of `Card` objects, representing the face-up purchaseable cards.

- A `bank` field, which is a `PebbleCollection` object, representing the bank.

- A `players` field, which holds a list of `GamePlayer` objects, which represents all the players in the game. Each `GamePlayer` object has:

  - an `id` field, holding an identification of the player (either as a networked user, a locally running bot, or some other option).

  - a `active` field, a `Boolean` representing whether the player is still in the game.

  - a `pebbles` field, which is a `PebbleCollection` object representing the pebbles available to the given player.

  - a `score` field, a `PositiveInt`, which represents the current score of this player.

- A `current_player` field, which is a positive integer index to the `players` list, representing the player whose turn it is.

- A `turn_state` field, which represents the portion of the current player's turn which it currently is (an enum between `START_OF_TURN`, `PURCHASING_CARDS`, and `GAME_OVER`).

**Wish List**

The following methods should be implemented to support this design:

```python
class OperationResult:
  success: bool # Represents the status of the operation
  error: str # If True, success. If False, there is an error string associated with the result.
  ...

# In the GameState class:
def get_repr_for_player(player_index: int):
  """
  Returns the portion of the game state available to the given player, formatted as a dictionary of primitive types (which can be sent as a JSON object).
  The object has same keys and structure as the attributes of the GameState, but with:
  - the player entries for the other players only having their id, status, and score
  - the deck field replaced by a deck_count field, representing the number of cards remaining.
  """
  ...

def get_pebble() -> OperationResult:
  """
  Attempts to have the current player take a random pebble from the bank. 
  Returns the status of the operation, and if it was successful, updates the game state accordingly.
  """
  ...

def use_equation(equation_index: int, left_to_right: bool) -> OperationResult:
  """
  Attempts to perform an exchange for the current player using the equation given by the provided index (either left to right if the provided Boolean is true, or right to left otherwise). 
  Returns the status of the operation, and if it was successful, updates the game state accordingly.
  """
  ...

def purchase_card(card_index: int):
  """
  Attempts to have the given player purchase the card given by the provided index. 
  Returns the status of the operation, and if it was successful, updates the game state accordingly.
  """
  ...
  ```