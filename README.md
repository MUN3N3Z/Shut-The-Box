# Shut-The-Box
The parameters for a given run will be given as command-line arguments as follows:

- The first command-line argument will be either `--one` or `--two` to indicate whether to solve for player one's expected number of wins or optimal move or for player two's.
- The second command-line argument will be either `--expect` or `--move` to indicate whether to calculate the expected wins for the player specified by the first argument or that player's optimal move.
- The position will be given as the third argument and will be a string of unique, increasing digits in the range 1 through 9 indicating which numbers are still open.
- For `--two`, the fourth argument will be a base-10 integer specifying player 1's score.
- For `--move` only, there will be an additional argument (fourth or fifth for `--one` or `--two` respectively) following the position giving the sum of the roll (as a base-10 integer) to determine the move for.