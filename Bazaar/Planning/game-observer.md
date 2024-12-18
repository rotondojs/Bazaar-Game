**TO:** Matthias Felleisen, Ben Lerner

**FROM:** Rishi Kanabar, John Rotondo

**DATE:** October 24, 2024

**SUBJECT:** Game Observer Design for the Bazaar Game

The protocol required to support observers in the game is fundamentally different compared to the Player Protocol defined [here](<https://course.ccs.neu.edu/cs4500f24/local_protocol.html#(part._g118837)>). One of the reasons for this this is that Player protocol is a synchronous protocol that requests a move from the player and processes it based on the move returned by the player.

The observer design on the other hand does _not_ have to be synchronous since the Referee (or any entity responsible for broadcasting game status information) does not depend on the responses sent by the observers of the game in order to continue the game. As a result, we propose a Publish-subscribe messaging model where the Referee or an "Observer Manager" is the publisher and all the observers are the subscribers of the communication.

The protocol will begin by the observers enlisting themselves as subscribers of the game of Bazaar (for observing the game).

```
Referee                         observer (o_1) . . . observer (o_n)

      |                                |                 |

      |  subscribe_observer(Observer)  |                 |

      | <----------------------------- |                 | % - subscribe to observe the game
```

Consequently, after the observers have successfully subscribed to observe the game, the Referee is responsible for asynchronously broadcasting key game changes such as player moves, game state changes, and game winners to all of the subscribers.

An example of an Observer is the one below where the observer has certain methods defined for the publisher to call in the case of these events.

```python
    class Observer(BaseModel):
    """Defines the class for all observers."""

        def on_player_action(self, player_action: PlayerAction, player: PlayerMechanism):
            """Triggered whenever a player performs a move."""
            raise NotImplementedError

        def on_game_state_change(self, state: GameState):
            """Triggered whenever the game state changes."""
            raise NotImplementedError

        def on_game_end(self, winner: list[str], misbehaved: list[str]):
            """Triggered when the game ends with the winner and the players that misbehaved."""
            raise NotImplementedError
```

The GameObserver class implements the observer interface. The Referee will have a publicly facing method called `subscribe_observer` that takes in an observer.

```python
observer = Observer()
referee.subscribe_observer(observer)
```

The Referee can delegate all of these calls to an Observer Manager that keeps track of multiple observers. It ensures that all registered observers receive game updates. This design also ensures that there is a separation of concern between the Referee and the pub-sub code related to broadcasting to all observers.

```python
    class ObserverManager(BaseModel):
        observers: list[Observer] = Field(default_factory=list)

        def notify_player_action(self, player_action: PlayerAction, player: PlayerMechanism):
            for observer in self.observers:
                observer.on_player_action(player_action, player)

        def notify_game_state_change(self, state: GameState):
            for observer in self.observers:
                observer.on_game_state_change(state)

        def notify_game_end(self, winner: list[str], misbehaved: list[str]):
            for observer in self.observers:
                observer.on_game_end(winner, misbehaved)
```

Finally, the responsibility of the Referee is to call the appropriate methods on the `ObserverManager` to ensure that all subscribers received game updates.
