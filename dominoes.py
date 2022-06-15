import random

MIN_WEIGHT = 0
MAX_WEIGHT = 6
PIECES_PER_PLAYER = 7
snake = []


def generate_domino_set():
    stock = []
    for i in range(MIN_WEIGHT, MAX_WEIGHT + 1):
        for j in range(i, MAX_WEIGHT + 1):
            piece = [i, j]
            stock.append(piece)
    random.shuffle(stock)
    return stock


def draw(stock):
    reserved = random.sample(stock, PIECES_PER_PLAYER)
    for piece in reserved:
        stock.remove(piece)
    return reserved


# To start the game, players determine the starting piece.
# The player with the highest double ([6,6] or [5,5] for example)
# will donate that domino as a starting piece for the game.
# After doing so, their opponent will start the game by going first.
def start_game(computer, human):
    max_double = [MAX_WEIGHT, MAX_WEIGHT]

    if max_double in computer:
        go(computer, max_double)
        return human

    if max_double in human:
        go(human, max_double)
        return computer

    c_doubles = find_double_dominoes(computer)
    h_doubles = find_double_dominoes(human)

    if len(c_doubles) == 0:
        go(human, max(human))
        return computer

    if len(h_doubles) == 0:
        go(computer, max(computer))
        return human

    max_computer_double = max(c_doubles)
    max_human_double = max(h_doubles)
    if max_computer_double > max_human_double:
        go(computer, max_computer_double)
        return human
    else:
        go(human, max_human_double)


def find_double_dominoes(pieces):
    doubles = []
    for piece in pieces:
        if piece[0] == piece[1]:
            doubles.append(piece)
    return doubles


def has_double_dominoes(domino_set):
    for piece in domino_set:
        if piece[0] == piece[1]:
            return True
    return False


def go(player, piece: list):
    snake.append(piece)
    player.remove(piece)


def print_status(stock, computer, human, next_player):
    print('=' * 70)
    print(f'Stock size: {len(stock)}')
    print(f'Computer pieces: {len(computer)}\n')
    print(*snake)
    print(f'\nYour pieces:')
    for i, p in enumerate(human):
        print(f'{i + 1}: {p}')

    if next_player == computer:
        status = 'Computer is about to make a move. Press Enter to continue...'
    else:
        status = "It's your turn to make a move. Enter your command."
    print(f'\nStatus: {status}')


def play():
    # Domino piece is double if the two numbers written on it are equal
    # If no one has a double domino, the pieces are reshuffled and redistributed.
    while True:
        stock = generate_domino_set()
        computer = draw(stock)
        human = draw(stock)
        if has_double_dominoes(computer) or has_double_dominoes(human):
            break
    next_player = start_game(computer, human)
    print_status(stock, computer, human, next_player)


if __name__ == '__main__':
    play()
