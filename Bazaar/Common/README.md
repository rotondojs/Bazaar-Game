This folder contains the shared classes that represent the game objects of the Bazaar game. The goal of having this folder as a separate package is to enable various other packages (for instance, player code, referee code, or other systems) to reference this package as a shared understanding of the game architecture.

This folder contains:

- pebble_collection.py, which contains the PebbleCollection class, representing a set of colored pebbles, as well as the Color enum for all colors a pebble can have, and the related static constants to support those definitions.

- cards.py, which contains the Card class, representing a purchasable card with a cost of five pebbles of some distribution of colors, which may or may not have a face printed on it.

- equations.py, which contains the Equation class, representing an Equation which can be used to convert between different type of pebbles, as well as the EquationTable class, which holds a list of available Equations.

- pygame_rendering.py, which contains static helper methods to render these game objects as Pygame surfaces, to aid in the construction of a GUI.

- turn_section.py, which contains the TurnSection class, an enumeration representing the various states the game can be in.

- game_player.py, which contains the GamePlayer class, which represents the data needed to represent a player in Bazaar as seen by the referee.

- turn_state.py, which contains the TurnState class, a representation of the game state as available to a single player.

- deserializer.py, a utility class for deserializing game data into Bazaar game objects.

- serializer.py, a utility class for serializing Bazaar game objects into JSON-compatible formats.

The unit tests for these methods are contained in the Tests folder, and can be run using the xtest executable in the Bazaar directory. 
Equations and Cards are entirely separate from each other, but both rely on PebbleCollections to represent their sides and cost respectively. The game state representation holds both the EquationTable available to the player and the Cards which can be purchased.