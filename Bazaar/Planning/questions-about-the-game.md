**TO:** Matthias Felleisen, Ben Lerner

**FROM:** Rishi Kanabar, Ethan Saff

**DATE:** September 11, 2024

**SUBJECT:** Questions about the Bazaar Game

Based on the provided description for the Bazaar Game, we would like to clarify the following points, to ensure our implementation accurately follows the game rules:

1.  How are the 20 cards for the game selected?  

There are 6250 possible valid cards (5 pebbles, each one of 5 colors, with or without a face), but only 20 cards are used in each game. 

2.  If multiple cards are bought in one turn, are they scored at once or separately?

If a player buys multiple cards in a single action, it was unclear to us whether the purchases were all scored based on the player's final number of pebbles held, or whether each card was scored based on the number of pebbles the player had immediately after purchasing it.

3.  Can a player perform an equation multiple times in one turn?

If this is possible, then a player can repeatedly perform an equation in alternating directions (i.e. with an equation 1 red = 2 blue, trading 1 red for 2 blue, then 2 blue for red, then repeating), thus immediately ending the game by emptying the deck, with this action being available as soon as a single exchange is possible.