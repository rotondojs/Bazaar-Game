Pair: amazing-squirrels \
Commit: e6629de1201d15b657df7ffc65174ccbd1af6de \
Score: 124/345 \
Grader: Lisa Jiang

### README
- [-10]: README in Bazaar/Referee doesn't contain the new file observer.java
- [-20]: README in Bazaar/Referee doesn't explain how the Referee and Observer interact. These top-level explanations are usually needed in your code walks anyway.

### Code Inspection
- [-10]: Referee should take in an Observer interface instead of hard-wiring it to a concrete Observer class
- [-8]: missing Observer purpose statement. Purpose statement should explain how the observer receives info/interact with the referee. Less penalty for honesty.
- [-8]: missing Observer purpose statement for how its view works: i.e.: what UI toggles to the next state, what UI feature saves the state, etc. Less penalty for honesty.
- [+0]: Observers are untrusted. Code should protect all calls to observers in the referee to prevent an "untrustworthy observer" from tearing down the whole game.

  ### Design
  - [-5]: interactions between referee and players should go through a remote proxy. The spec asked to read up on the remote proxy design pattern.
  - [-5]: no mention of serializing/deserializing JSON for remote communications between referee and players
  - [-5]: no mention of a client that signs up to join the game on behalf of the players. No mention of a server that starts the tcp connection on behalf of referee.
 
  ### In-person demo
  [0/150]

free-text
