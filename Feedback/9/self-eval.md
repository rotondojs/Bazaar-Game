The commit we tagged for your submission is 7657751628d22ebe5fe391e8aa1a2753765cffe.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F24/amazing-squirrels/tree/7657751628d22ebe5fe391e8aa1a2753765cffe

## Self-Evaluation Form for Milestone 9

Indicate below each bullet which file/unit takes care of each task.

### Programming Task 

For `Bazaar/Server/player`,

- explain how it implements the exact same interface as `Bazaar/Player/player`

`ProxyPlayer` in `proxy_player.py` extends `PlayerMechanism` and overrides the key methods such as, 
`setup`, `request_pebble_or_trades`, `request_cards`, `win`.
This enables communication over TCP sockets while preserving the expected interface.
we should create an interface and have both inherit from the interface instead

https://github.khoury.northeastern.edu/CS4500-F24/amazing-squirrels/blob/7657751628d22ebe5fe391e8aa1a2753765cffe4/Bazaar/Server/proxy_player.py#L13

- explain how it receives the TCP connection that enables it to communicate with a client

The `ProxyPlayer` constructor accepts a socket instance

https://github.khoury.northeastern.edu/CS4500-F24/amazing-squirrels/blob/7657751628d22ebe5fe391e8aa1a2753765cffe4/Bazaar/Server/proxy_player.py#L17

- point to unit tests that check whether it writes (proper) JSON to a mock output device

We do not have any unit tests that check whether it writes (proper) JSON to a mock output device

For `Bazaar/Client/referee`,

- explain how it implements the same interface as `Bazaar/Referee/referee`

The `player_json_interface` has a very different interface. It calls the player in the same way that the normal referee calls a player, but has no `run` method, which is the only method in the interface for the `Referee`.

https://github.khoury.northeastern.edu/CS4500-F24/amazing-squirrels/blob/7657751628d22ebe5fe391e8aa1a2753765cffe4/Bazaar/Client/player_json_interface.py#L10
- explain how it receives the TCP connection that enables it to communicate with a server

the socket remains in the `client` and the relevant data is passed to the `player_json_interface` through method calls.

https://github.khoury.northeastern.edu/CS4500-F24/amazing-squirrels/blob/7657751628d22ebe5fe391e8aa1a2753765cffe4/Bazaar/Client/client.py#L16
- point to unit tests that check whether it reads (possibly broken) JSON from a mock input device

No such unit tests.

For `Bazaar/Client/client`, explain what happens when the client is started _before_ the server is up and running:

- does it wait until the server is up (best solution)
- does it shut down gracefully (acceptable now, but switch to the first option for 10)

The client does nothing on construction, but will attempt to connect when the `connect` method is called. Currently, it will raise an exception if it fails to connect to the server.

https://github.khoury.northeastern.edu/CS4500-F24/amazing-squirrels/blob/7657751628d22ebe5fe391e8aa1a2753765cffe4/Bazaar/Client/client.py#L28

For `Bazaar/Server/server`, explain how the code implements the two waiting periods. 

The server has a method with a loop that checks how many waiting periods have happened, allowing the number of waiting periods to be easily changed. 

https://github.khoury.northeastern.edu/CS4500-F24/amazing-squirrels/blob/7657751628d22ebe5fe391e8aa1a2753765cffe4/Bazaar/Server/server.py#L65
### Design Task 

For design task 1,

- did you make sure to separate the changes into one for the knowledge
  about players and one for the rule book? Why is this separation critical?

Yes. The separation is critical because there are changes to be made to different parts of the code base.

https://github.khoury.northeastern.edu/CS4500-F24/amazing-squirrels/blob/7657751628d22ebe5fe391e8aa1a2753765cffe4/Bazaar/Planning/bonus.md

For design task 2, 

- did you consider changes to the data representation pebbles?

Yes.
- would this change induce changes to wallets and cards?

No.

For the reflection on design tasks, you may wish to point to relevant
pieces of code to justify your responses. There was no need to
implement anything so the _old_ code is all the TAs need. 

### Form of Feedback


The ideal feedback for each of these three points is a GitHub
perma-link to the range of lines in a specific file or a collection of
files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* realize these pieces of functionality, say so.

