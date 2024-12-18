The commit we tagged for your submission is d1731e9e55c08b9cc611dfba7d71a7fffae4213.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F24/amazing-squirrels/tree/d1731e9e55c08b9cc611dfba7d71a7fffae4213

## Self-Evaluation Form for Milestone 8

Indicate below each bullet which file/unit takes care of each task:

- did you consider what role an observer plays in the overall system?

`observer.py` manages game states, saves images of states, and displays them. 
This file is responsible for maintaining a record of each game state and visualizing it on demand, 
providing dev ops with insights into the game as it progresses.

[https://github.khoury.northeastern.edu/CS4500-F24/amazing-squirrels/blob/main/Bazaar/Referee/observer.py]

- concerning the modifications to the referee: 

  - is the referee programmed to the observer's interface or is it hardwired?

In `referee.py`, the observer interaction is designed to be flexible. 
The referee class accepts observers as a list parameter (`self.observers`), 
initializing them with the starting `game_state` and 
invokes them by calling methods like `receive_state` and `game_over` dynamically.
So the observer is programmed to an interface rather than hardwired, making it adaptable.

[https://github.khoury.northeastern.edu/CS4500-F24/amazing-squirrels/blob/main/Bazaar/Referee/referee.py]

  - if an observer is desired, is every state per player action sent to the observer? Where? 

In `referee.py`, within the `notify_observers` method, 
the referee sends every updated game state to each observer after specific game actions, 
like pebble trades or card purchases. This ensures observers are updated on all state transitions.

[https://github.khoury.northeastern.edu/CS4500-F24/amazing-squirrels/blob/main/Bazaar/Referee/referee.py]

  - if an observer is not desired, how does the referee avoid calls to the observer?

If no observer is provided, `self.observers` remains empty or none, 
and the `notify_observers` method simply does not trigger any observer methods. 
This design makes observer interaction conditional, 
ensuring that there are no unnecessary calls if no observer is specified.

[https://github.khoury.northeastern.edu/CS4500-F24/amazing-squirrels/blob/main/Bazaar/Referee/referee.py]

- concerning the implementation of the observer:

  - does the purpose statement explain how to program to the
    observer's interface? 

The purpose statement in `observer.py` provides an overview of the class's functions 
but does not explicitly mention programming to the interface. 
However, referee initializes them with the starting `game_state` and 
invokes them by calling methods like `receive_state` and `game_over`.
These can serve as a reference for the expected methods to implement an observer.

example of how to initialize an `Observer`:
ob1 = Observer(GameStateFactory(player_count=3).create())
- `GameStateFactory` creates a `GameState`

[https://github.khoury.northeastern.edu/CS4500-F24/amazing-squirrels/blob/main/Bazaar/Referee/referee.py]

[https://github.khoury.northeastern.edu/CS4500-F24/amazing-squirrels/blob/main/Bazaar/Referee/observer.py]

  - does the purpose statement explain how a user would use the
    observer's view? Or is it explained elsewhere? 

`observer.py` does not directly explain how a user would utilize the observer's view. 
However, functions like `display_saved_states`, `save_state_as_png`, and `save_states` 
will allow users to view all states of a game on the GUI as png images.

To use an Observer's view left and right arrow keys are used to switch between png images, 
pressing the 's' key saves a png state in JSON format

Example of the code where key presses are recognized:
```python
if event.type == pygame.QUIT:
    running = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s:
            self.save_state()
        elif event.key == pygame.K_LEFT:
            if self.display_index < self.save_index:
                self.display_index += 1
        elif event.key == pygame.K_RIGHT:
            if self.display_index > 0:
                self.display_index -= 1
```
Example of JSON save format:
```json
{"bank": null, 
  "visibles": [
      {"face?": true, "pebbles": ["WHITE", "WHITE", "GREEN", "GREEN", "YELLOW"]}, 
      {"face?": true, "pebbles": ["RED", "WHITE", "BLUE", "YELLOW", "YELLOW"]}, 
      {"face?": false, "pebbles": ["RED", "WHITE", "WHITE", "GREEN", "YELLOW"]}, 
      {"face?": true, "pebbles": ["WHITE", "WHITE", "GREEN", "YELLOW", "YELLOW"]}
  ], 
  "cards": [
      {"face?": false, "pebbles": ["RED", "WHITE", "WHITE", "BLUE", "YELLOW"]}, 
      {"face?": true, "pebbles": ["RED", "BLUE", "BLUE", "GREEN", "YELLOW"]}, 
      {"face?": true, "pebbles": ["BLUE", "BLUE", "BLUE", "GREEN", "YELLOW"]}, 
      {"face?": true, "pebbles": ["RED", "RED", "WHITE", "BLUE", "BLUE"]}, 
      {"face?": true, "pebbles": ["RED", "WHITE", "BLUE", "BLUE", "YELLOW"]},
  ], 
  "players": [
      {"score": 0, "wallet": []}, 
      {"score": 0, "wallet": []}, 
      {"score": 0, "wallet": []}
  ]
}
```
[https://github.khoury.northeastern.edu/CS4500-F24/amazing-squirrels/blob/main/Bazaar/Referee/observer.py]

The ideal feedback for each of these three points is a GitHub
perma-link to the range of lines in a specific file or a collection of
files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* realize these pieces of functionality, say so.

