Pair: amazing-squirrels \
Commit: 9af5498a035437f382180e3bb3d18592cdb15a3 \
Score: 80/120 \
Grader: Daniel Allex

- [80/120] Program Inspection
  - [0/20] Helpful modifications.md file
    - Missing modifications.md in Bazaar/Planning
  - [20/20] functionally abstracting the referee over a bonus policy
  - [0/20] award-bonus functionality, located in the (knowledge about) player module
    - Rule book should not be awarding the bonus points / updating the game state -- it should at most be deciding the number of bonus points to give, if any
  - [20/20] referee's knowledge about the player must also come with a field for the purchased cards and with a modification of the method that evaluates a player's request to buy cards
  - [20/20] check that the player's cards display the required pebbles is a binary "method", consuming both a list of pebbles (or pebble colors) and the cards
  - [20/20] unit tests