**TO:** Matthias Felleisen, Ben Lerner

**FROM:** Galen Wu, John Rotondo

**DATE:** November 7, 2024

**SUBJECT:** Remote Design for the Bazaar Game

This protocol will include:

Player Registration: Players register with the referee, indicating that they are ready to join a game. 
Players register with the referee by sending a registration request, including necessary identification details.

```json
{
  "type": "register_player",
  "data": {
    "player_name": "string",
    "connection_info": {
      "ip": "string",
      "port": "integer"
    }
  }
}
```

Game Launch: The referee organizes a game session once a minimum number of players is gathered. 
When the required number of players is registered, the referee initiates the game. 
Each player receives a message with the game's start information and other players' details.

```json
{
  "type": "game_start",
  "data": {
    "game_id": "string",
    "starting_turn_state": {
      "bank": [],
      "visibles": [],
      "cards": [],
      "players": []
    }
  }
}
```

In-Game Interactions: Players interact with the referee during the game for turn-based actions. 
The referee requests moves from the Players, verifies and applies them to the game state, 
then broadcasts updated states to all players. If a player takes to long to respond they will be kicked for inactivity.

Referee to Player interaction:

request_type is one of 
 - "request_pebbles_or_exchange" 
 - "request_cards"
```json
{
  "type": "request_type",
  "data": {
    "game_state": {
      "bank": [],
      "visibles": [],
      "cards": [],
      "players": []
    }
  }
}
```

Result Reporting: After the game concludes, the referee reports the results to all participants. 

```json
{
  "type": "game_result",
  "data": {
    "game_id": "string",
    "result": [
      {
        "game_state": {
          "bank": [],
          "visibles": [],
          "cards": [],
          "players": []
        },
        "winners": [
          {
            "player_id": "string",
            "player_name": "string",
            "score": "integer"
          }
        ],
        "kicked players": [
          {
            "player_id": "string",
            "player_name": "string"
          }
        ]
      }
    ]
  }
}
```

Sequence Diagram:
```
Player 1            Referee            Player 2
   |                   |                   |
   |----register-----> |                   |
   |<--acknowledgment--|                   |
   |                   |                   |
   |                   |<----register----- |
   |                   |--acknowledgment-->|
   |                   |                   |
   |<-------game_start (broadcast)-------->|
   |                   |                   |
   |                   |                   |<---+
   |<--request_action--|                   |    |
   |---player_action-->|                   |    |
   |                   |--state_update-->  |    |
   |<--request_action--|                   |    |
   |---player_action-->|                   |    |
   |                   |--state_update-->  |    | loop while the game is running
   |                   |                   |    |
   |                   |--request_action-->|    |
   |                   |<--player_action---|    |
   |<--state_update--- |                   |    |
   |                   |--request_action-->|    |
   |                   |<--player_action---|    |
   |<--state_update--- |                   |    |
   |                   |                   |----+
   |                   |                   |
   |<-------game_result (broadcast)------->|
```