# domino
### Hyperskill project

As you might know, a domino is a playing piece that is characterized by the two numbers written on it. The numbers are integers and can range from 0 to 6. A single domino piece has no orientation, so, a full domino set (that includes all the possible pairs of numbers) will have 28 unique dominoes.

You may think that there should be 7*7=49 dominoes in total. However, this is not the case because the combinations like [1,2] and [2,1] are the same domino, not two separate ones.

#### Description
To play domino, you need a full domino set and at least two players. In this project, the game is played by you and the computer.

At the beginning of the game, each player is handed 7 random domino pieces. The rest are used as stock (the extra pieces).

To start the game, players determine the starting piece. The player with the highest double ([6,6] or [5,5] for example) will donate that domino as a starting piece for the game. After doing so, their opponent will start the game by going first. If no one has a double domino, the pieces are reshuffled and redistributed.

The player should be able to see the domino snake, the so-called playing field, and their own pieces. It's a good idea to enumerate these pieces because throughout the game the player will be selecting them to make a move.

Two things must remain hidden from the player: the stock pieces and the computer's pieces. The player should not be able to see them, only the number of pieces remaining.

#### Objectives
1. Generate a full domino set. Each domino is represented as a list of two numbers. A full domino set is a list of 28 unique dominoes.
2. Split the full domino set between the players and the stock by random. You should get three parts: Stock pieces (14 domino elements), Computer pieces (7 domino elements), and Player pieces (7 domino elements).
3. Determine the starting piece and the first player. If the starting piece cannot be determined (no one has a double domino), reshuffle, and redistribute the pieces.

4. Print the header using seventy equal sign characters (=).
5. Print the number of dominoes remaining in the stock – Stock size: [number].
6. Print the number of dominoes the computer has – Computer pieces: [number].
7. Print the domino snake. At this stage, it consists of the only starting piece.
8. Print the player's pieces, Your pieces:, and then one piece per line, enumerated.
9. Print the status of the game:
    - If status = "computer", print "Status: Computer is about to make a move. Press Enter to continue..."
    - If status = "player", print "Status: It's your turn to make a move. Enter your command."
    - Note that both these statuses suppose that the next move will be made, but at this stage, the program should stop here. We will implement other statuses (like "win", "lose", and "draw") in the stages to come.
