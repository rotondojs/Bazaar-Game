**TO:** Matthias Felleisen, Ben Lerner

**FROM:** Rishi Kanabar, Ethan Saff

**DATE:** September 11, 2024

**SUBJECT:** Sprint Plan for the Bazaar Game

# Sprints

To begin this project, we would like to propose the following series of sprints, each focused on a separate component of the project:

## Sprint 1
The first sprint will be centered on the format by which the referee sends game data to the players, as well as the game logic implemented in the referee. As part of this sprint, we will write:
- A specification for the JSON data concerning the game state and player actions which is sent from and to the referee.
- A referee class capable of receiving this JSON data and responding with data indicating the new game state, following the described game rules. 

At the end of the first sprint, we will have completed a referee implementation, which can be given game commands and outputs resulting game states using our JSON interface, with the logic of the game implemented inside the referee.

## Sprint 2
The second sprint will be centered on the player-referee interface, including the implementation of a sample player class (which follows a simple algorithm) and the implementation of a server to send data between the players and referee. 
As part of this sprint, we will implement:
- A sample player class, which takes the game state output and outputs player commands, with both formatted in JSON as described in Sprint 1.
- An interface which enables the referee and player(s) to send game state and commands to each other.

At the end of the second sprint, we will have a player interface and sample player capable of fully completing a game once manually connected to each other and to the referee designed in Sprint 1.

## Sprint 3
The third sprint will be centered on the game setup and connection process, including initial setup, game end, and observers. 
As part of this sprint, we will implement:
- The game setup, including the player locating the server, the server finding players, the server initializing a referee for a new game, and the server establishing connection between the players and referee
- The server communicating the game ending, as well as player disconnections and expulsions.
- The broadcasting of player events and referee actions to other players and observers in the game, based on the "visibility" of that event to the player / observer. 

At the end of the third sprint, we will have implemented the process of players finding and joining games (including setting up a referee for each game), observers finding games, and the interface broadcasting data to observers, as well as accounting for player connections, disconnections, and expulsions for illegal actions.
