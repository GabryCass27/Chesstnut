# Chesstnut
Chesstnut is a chess engine designed in the Python language.
The project was born on 24 December 2022 with the aim of bringing more and more people closer to the world of chess.

# Project development phases
The project starts in December 2022. The development phases are divided into: 
* __Documentation__: via Chat-GPT I documented myself regarding algorithms, learning techniques and which programming language to adopt (Python). For this documentation, YouTube was also used for the code sections and the implementation of the algorithms (time 1/2 weeks);

* __Coding__: this is where we start to flesh out what was left in the form of research. This phase is divided into 10 steps, which we will report on below (for more info follow [Eddie Sharick's Youtube channel](https://www.youtube.com/channel/UCaEohRz5bPHywGBwmR18Qww));

# Tools
* [Python 3.11](https://www.python.org/)
* [Pygame 2.1.3.dev8](https://www.pygame.org) ```pip install pygame```

# Coding
1. Search for and download images of the individual pieces (king, queen, rook, bishop, knight, pawn);
2. Creating an 8x8 matrix;
3. Creating the software window and chessboard (GUI);
4. Loading the images within the matrix;
5. Writing the part of the code that allows the pieces to move;
6. Checking the validity of the movements;
7. Implementation of the basic chess rules (checkmate, checkmate and draw);
8. Implementation of advanced rules (en-passant, castling and promotion);
9. Implementation of AI;
10. Graphical enhancements;
<br><br>

## Algorithms
### NegaMax algorithm
The NegaMax algorithm is a variant of the Minimax algorithm used for finding the best move in a zero-sum game such as chess. The goal of the algorithm is to find the best move for a player, maximising his advantages and minimising those of his opponent.
<br>
### Alpha-Beta pruning algorithm
The Alpha-Beta Pruning algorithm is an optimisation technique used in the NegaMax algorithm to reduce the number of searches in the move tree by eliminating branches that do not affect the final result, thus reducing the computational time for searching.
<br><br>

# Instructions
1. Clone this repository.
2. Select whether you want to play versus computer, against another player locally, or watch the game of engine playing against itself by setting appropriate flags in lines 52 and 53 of `Main.py`.
3. Run `Main.py`.
Enjoy the game!

Sic:

* Press `⬅️ Key` to undo a move.
* Press `r` to reset the game.

# Further development ideas
1. Ordering the moves (ex. looking at checks and/or captures) should make the engine much quicker (because of the alpha-beta pruning).
2. Keeping track of all the possible moves in a given position, so that after a move is made the engine doesn't have to recalculate all the moves.
3. Evaluating kings placement on the board (separate in middle game and in the late game).
4. Book of openings.
5. Stalemate on 3 repeated moves or 50 moves without capture/pawn advancement.
6. Decent menu to select player vs player/computer.
7. Draw arrows (like Chess.com).
8. Make PGN file.
9. Match analysis (like Chess.com).

# More Info:
* [Document Chesstnut EN](https://www.canva.com/design/DAFl7PPa3j4/1ERQk_2xrK8qOqiZOn403g/view?utm_content=DAFl7PPa3j4&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink) 
* [Document Chesstnut IT](https://www.canva.com/design/DAFl7VHCSlo/Z0u2aX2XwaNZ1tZ6A1M9vw/view?utm_content=DAFl7VHCSlo&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink)

Contact:
cassanitigabriele06@gmail.com
