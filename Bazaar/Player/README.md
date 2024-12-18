This folder contains the shared classes that represent the player objects of the Bazaar game. The goal of having this folder as a separate package is to enable various other packages (for instance, referee code, or other systems) to reference this package as a shared understanding of the player.

This folder contains:

- player_action.py, which contains the ActionType enum class, an enumeration of possible action types in the game that can be made by the player, as well as the \_PlayerActionOptions which represents the options for a player's action, and the PlayerAction which represents a player's action in the game.

- Strategy.py, which contains the StrategyNode class, which is a core data structure that represents a state in the decision tree for the strategy algorithm, and the Strategy class which produces the most optimal moves by evaluating possible moves based on the state of the game.

- `mechanism.py` contains player protocol related code to make a move in the game of Bazaar based on a passed in game strategy. It follows the Player Protocol detailed [here](<https://course.ccs.neu.edu/cs4500f24/local_protocol.html#(part._g118836)>).

The unit tests for these methods are contained in the Tests folder, and can be run using the xtest executable in the Bazaar directory.
This folder also contains a diagram of the player protocol that represents how a player will interact with the Referee, and how an AI player will interact with Strategy, and this is located in the static folder.
