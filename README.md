# superNimGame
The file consists of programming a Python implementation of a player that plays Super Nim Game
## The Rules for Super-Nim
The game of Super-Nim is played by two players, max and min. The game situation is given by a number
of heaps with sticks and a scoreboard for both players.
## Moves
Given a game state with a number of heaps, each of them containing a non-zero number of sticks, a move
consists of one of the following:
1. taking a heap and put it on another heap, as long as it does not have the same size; when you
exceed 10 sticks on a heap, cap the number at 10. E.g. if you have heaps (2,4,2,5,7), you can
put the first heap onto the second, getting (6,2,5,7).
Or you can put the second heap onto the last instead, getting (2,2,5,10). What you cannot do is
to put the first heap onto the third as they have the same size.
2. alternatively, you can perform a Collatz-Ulam step on the heap, i.e.:
(a) for a heap that has an odd number of sticks n, you can replace it by 3n + 1 sticks. The
number is not capped. I.e., if you have heaps (2,4,2,5,7), you can replace the 4th heap by
(2,4,2,16,7).
(b) for a heap that has an even number of sticks n, you can split it into two heaps of half size n=2.
E.g. the second heap in (2,4,2,5,7) can be split to give (2,2,2,2,5,7).
If you split a heap of size 2, you get two 1-stick heaps | these are removed and converted into
2 points, for the player that made the move. So, if max played, max gets two points, if min
plays, min gets two points, and the 1-stick heaps are removed.
For instance, if min splits the first heap in (2,4,2,5,7), min gets 2 points, and the remaining
heap is (4,2,5,7).
(c) the game ends when there are no more sticks to move.
(d) the purpose is for the max player to accumulate as many as possible points, and same for the
min player. Both points are accumulated separately, the winner is determined by having the
most points.
1(e) note that the game may not necessarily end and cycles are possible. In this case, whoever
keeps the most points is considered the winner (we do not require a hard criterion here).
