This folder contains the classes that represent the game objects of the Bazaar game which are used to define the referee implementation.

This folder contains:

- `referee.py` contains all the code for the Referee in the game of Bazaar. Its main purpose is to act as a proxy
- between the players and the game state, validating the moves through the rule book. The referee also informs any
- observers that are registered to the referee of the game state after each turn. Observers may subscribe to the game by
- calling `referee.subscribe` and passing themselves to the referee.

- game_state.py, which contains the GameState class, a representation of the game state as available to the referee, holding all players in the game, the bank, the equation table used for exchanges, the cards available for purchase, and the cards in the deck.

- pygame_rendering.py, which contains static helper methods to render these game objects as Pygame surfaces, to aid in the construction of a GUI.

- observer.py, which contains the Observer class, which represents the data needed to represent and render all states of a game for an observer in Bazaar.

- IObserver.py, an interface for a game observer handling game states and game over events.

- gui_test.py, used to test generation and rendering (as described below).

The unit tests for these methods are contained in the Tests folder, and can be run using the xtest executable in the Bazaar directory.
This folder also contains the file gui_test.py, which when run will generate and render a new game state, and enable the user to test the game logic by performing game actions using the following key combinations (all indices start from 1, and 0 is used to represent 10):

- g to get a pebble

- [1-5]p to purchase the numbered card from the tableau

- [1-0]e to perform an exchange using the given equation (press r to use the equation right-to-left, otherwise the equation will be used left-to-right)

- n to end turn

- [1-8]k to kick the indicated player

Note that since this is a test program and not an implementation intended for delivery, there is no error handling, and the program will crash if an invalid action is attempted.
