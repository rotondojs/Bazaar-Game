The commit we tagged for your submission is 48b9cd1e6982874571c00395c8f40ba575859ca.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F24/amazing-squirrels/tree/48b9cd1e6982874571c00395c8f40ba575859ca

## Self-Evaluation Form for Milestone 10

The ideal answer for each of the following questions consists of two or three sentences.


1. What role do purpose statements play? 
Purpose statements clarify the objective of a function or class
by explicitly stating what it is designed to do. 
They guide developers in understanding the code's intent, 
making it easier for others to pick up on the purpose of the code.




2. How do unit tests help with software development?
Unit tests validate the correctness of classes or methods 
by ensuring they behave as expected throughout various situations. 
They help catch bugs early and provide confidence in the code's reliability.




3. Which milestone was the most difficult to unit-test?
Milestone 6 was the most difficult to test because we had to test Referee.
We had to test:
   - Asynchronous Behavior: The Referee relies on asynchronous methods to interact with player `mechanisms` and 
   `observers`, requiring the use of asynchronous testing frameworks and careful handling of concurrency.

   - Extensive Dependencies: The Referee interacts with several interconnected components, such as `PlayerMechanism`, 
   `RuleBook`, and `GameState`, each of which has its own state and behavior. 
   Mocking these dependencies accurately was hard.




4. Did you struggle with your TAHBPL or was the language helpful?
It felt ambiguous, especially if the documentation or naming conventions aren't clear. 
While the testing all easy paths is straightforward, 
it became challenging with edge cases.




5. What would you differently if you could send a message to your younger self in early September 2024? 
We would probably try next time to use a different language like java. 
Also, working with pydantic made initialization of classes more involved.
Finally, We would not index through the cards and instead use the actual cards instead of indexing through them.







