import random

MIN_WEIGHT = 0
MAX_WEIGHT = 6
PIECES_PER_PLAYER = 7
END_GAME_COUNTER = 8
COMPUTER = 'computer'
HUMAN = 'human'

snake = []
stock = []


def generate_domino_set():
    for i in range(MIN_WEIGHT, MAX_WEIGHT + 1):
        for j in range(i, MAX_WEIGHT + 1):
            stock.append([i, j])
    random.shuffle(stock)
    return stock


def draw():
    reserved = random.sample(stock, PIECES_PER_PLAYER)
    for piece in reserved:
        stock.remove(piece)
    return reserved


def start(players):
    """
    To start the game, players determine the starting piece.
    The player with the highest double ([6,6] or [5,5] for example)
    will donate that domino as a starting piece for the game.
    After doing so, their opponent will start the game by going first.
    """
    computer = players[COMPUTER]
    human = players[HUMAN]

    max_computer_double = find_max_double_domino(computer)
    max_human_double = find_max_double_domino(human)

    if max_computer_double > max_human_double:
        update_dominoes_sets(computer, max_computer_double)
        return HUMAN
    else:
        update_dominoes_sets(human, max_human_double)
        return COMPUTER


def find_max_double_domino(pieces):
    doubles = []
    for piece in pieces:
        if piece[0] == piece[1]:
            doubles.append(piece)
    return [] if len(doubles) == 0 else max(doubles)


def has_double_dominoes(domino_set):
    return any(piece[0] == piece[1] for piece in domino_set)


def move(player: str, dominoes: list):
    chosen_piece = None
    if player == COMPUTER:
        next_player = HUMAN
        input('Status: Computer is about to make a move. Press Enter to continue...\n')
        chosen_piece = next(filter(is_correct_domino, dominoes), None)
    else:
        next_player = COMPUTER

        print("Status: It's your turn to make a move. Enter your command.")
        while True:
            try:
                index = abs(int(input())) - 1
            except ValueError:
                print('Invalid input. Please try again.')
                continue

            # if index == -1 then skip a turn
            if index == -1:
                break

            if index >= len(dominoes):
                print('Invalid input. Please try again.')
                continue

            chosen_piece = dominoes[index]
            if is_correct_domino(chosen_piece):
                break
            else:
                print('Illegal move. Please try again.')
                continue

    left_side = False
    if chosen_piece is not None:
        left_side = set_to_left_side(chosen_piece)
        reverse_domino(chosen_piece, left_side)
    update_dominoes_sets(dominoes, chosen_piece, left_side)
    return next_player


def set_to_left_side(piece):
    return snake[-1][-1] not in piece


def is_correct_domino(piece):
    return any(num == snake[0][0] or num == snake[-1][-1] for num in piece)


def reverse_domino(piece: list, left_side: bool):
    if left_side and piece[0] == snake[0][0] or not left_side and piece[-1] == snake[-1][-1]:
        piece.reverse()


def update_dominoes_sets(player_set, piece=None, left_side=False):
    # skip a turn
    if piece is None:
        if len(stock) != 0:
            index = random.choice(stock)
            player_set.append(index)
            stock.remove(index)
        return

    if left_side:
        snake.insert(0, piece)
    else:
        snake.append(piece)
    player_set.remove(piece)


def print_status(players):
    print('=' * 70)
    print(f'Stock size: {len(stock)}')
    # print(f'Stock size: {stock}')
    print(f'Computer pieces: {len(players[COMPUTER])}\n')
    # print(f'Computer pieces: {players[COMPUTER]}\n')
    if len(snake) > 6:
        print(*snake[:3], '...', *snake[-3:])
    else:
        print(*snake)
    print(f'\nYour pieces:')
    for i, p in enumerate(players[HUMAN]):
        print(f'{i + 1}: {p}')
    print()


def end_game(players, next_player):
    """
    The end-game condition can be achieved in two ways:

    - One of the players runs out of pieces. The first player to do so is considered a winner.
    - The numbers on the ends of the snake are identical and appear within the snake 8 times. 
       For example, the snake below will satisfy this condition:
      [5,5],[5,2],[2,1],[1,5],[5,4],[4,0],[0,5],[5,3],[3,6],[6,5]
      These two snakes, however, will not:
      [5,5],[5,2],[2,1],[1,5],[5,4],[4,0],[0,5]
      [6,5],[5,5],[5,2],[2,1],[1,5],[5,4],[4,0],[0,5],[5,3],[3,1]
      If this condition is satisfied, it is no longer possible to go on with this snake.
      Even after emptying the stock, no player will have the necessary piece.
      Essentially, the game has come to a permanent stop, so we have a draw.
    """
    if len(players[next_player]) == 0:
        winner = 'The computer won' if next_player == COMPUTER else 'You won'
        print(f'Status: The game is over. {winner}!')
        return True

    if snake[0][0] == snake[-1][-1] and \
            sum(num == snake[0][0] for piece in snake for num in piece) == END_GAME_COUNTER:
        print("Status: The game is over. It's a draw!")
        return True
    return False


def play():
    """
    Domino piece is double if the two numbers written on it are equal
    If no one has a double domino, the pieces are reshuffled and redistributed.
    """
    global stock
    while True:
        stock = generate_domino_set()
        players = {COMPUTER: draw(), HUMAN: draw()}
        if has_double_dominoes(players[COMPUTER]) or has_double_dominoes(players[HUMAN]):
            break

    next_player = start(players)

    while True:
        if end_game(players, next_player):
            break

        print_status(players)
        next_player = move(next_player, players[next_player])


if __name__ == '__main__':
    play()
