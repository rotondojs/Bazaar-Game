# Todo

**Moved to Completed**

# Completed

- Remove `EquationTable` from the `TurnState` and pass it around separately to better match the spec
  - [Commit](https://github.khoury.northeastern.edu/CS4500-F24/glistening-salamanders/commit/c68bc78563ff3db45c6d894cc543d746326ccd86)
  - **Commit Message**: `refactor: move equation table out of turn state and remove make move`
- Remove `make_move` method from `Strategy`
  - [Commit](https://github.khoury.northeastern.edu/CS4500-F24/glistening-salamanders/commit/c68bc78563ff3db45c6d894cc543d746326ccd86)
  - **Commit Message**: `refactor: move equation table out of turn state and remove make move`
- Define the lower and upper bound of pebbles in `Equation` so if someone were to configure the equations differently, they can pass it into the validator.
  - [Commit](https://github.khoury.northeastern.edu/CS4500-F24/glistening-salamanders/commit/519e99a847989a3959bb86a992dcd99b288e2dc2)
  - **Commit Message**: `chore: update validator `
- Introduce dependency injection for `RuleBook` in `Referee` / define it as a class variable that can be switched easily.
  - [Commit](https://github.khoury.northeastern.edu/CS4500-F24/glistening-salamanders/commit/388c90c6a889fea7a9541714ca8d46537b426f4d)
  - **Commit Message**: `feat: make rulebook a class variable for easier switching`
- Reduce _magic numbers_ in code (especially in `RuleBook`)
  - [Commit](https://github.khoury.northeastern.edu/CS4500-F24/glistening-salamanders/commit/117d7fd517f7ffac05f7bde67ee80a333363af2c)
  - **Commit Message**: `refactor: reduce magic numbers in code`
- Make use of `GameOver` exception to signal `GameOver` from the `RuleBook`
  - [Commit](https://github.khoury.northeastern.edu/CS4500-F24/glistening-salamanders/commit/50256947185274c674e909574cbef8f1a540d7ac)
  - **Commit Message**: `feat: throw gameover from rulebook to signal gameover`

# Impact of Proposed Changes

1. Change to the points awarded for purchasing cards

- **Difficulty**: 1 (Very Easy)
- **Explanation**: In order to change the points awarded, the maintainer of the code would have to modify the `ClassVar`s defined at the top of the `RuleBook` class that correspond to the scoring table in the spec. The number of constants changed would depend on the change to the table itself but we have _three_ constants defined for each scoring "bracket": the scoring cut-off, the points awarded for a card with a face, and the points awarded for a card without a face.

2. Change to Rules

- Make all basic Bazaar game constants configurable

  - **Difficulty**: 1 (Very Easy)
  - **Explanation**: It would be very easy to change the game constants since all of them are defined either in the `RuleBook` or are passed in the constructor of the `GameState` factory.

- Modify the strategies so that a player trades even if it cannot buy a card after the trade

  - **Difficulty**: 3 (Moderate)
  - **Explanation**: In order to allow trades even if the player cannot buy a card, the `Strategy` class, specifically the `request_pebble_or_trades` would have to change in a way where the check for whether a player can buy a card is removed. Moreover, we would have to modify the spec to document the best sequence of exchanges for a strategy when a player cannot buy a card.

- Add a rule that rewards players at the end of the game for buying cards with certain characteristics, say cards with just "red" pebbles.

  - **Difficulty**: 3 (Moderate)
  - **Explanation**: In order to support this, we would have to make _two_ key changes: one is ensuring that the `GamePlayer` object keeps track of the cards purchased by the player (right now we don't track this since with the current spec, we only care about the score resulting from buying the said card), and adding another method in the `RuleBook` class that will be called after the game is over to reward additional points (this will be called by the `Referee`).
