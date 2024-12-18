Proposal 1 - Patriotic scoring:

 - a GamePlayer would need to keep track of a list of Cards it has purchased to be checked later
 - the Referee would need to check each players list of purchased cards to see if they meet the condition after the game
is over, and before the winners are determined. If any player meets the condition their score would be increased by 10.

Proposal 2 - Glowing pebbles:
 - a Pebble class would be created which would be a Color and a boolean `glowing`
   - the constructor would presumably randomly produce glowing pebbles with some distribution
 - a PebbleCollection would need to hold Pebbles instead of Colors
 - every location that refers to the Colors in a PebbleCollection would need to be updated to work with Pebbles
 - the changes from Proposal 1 would also need to be implemented