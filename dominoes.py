import random

MIN_WEIGHT = 0
MAX_WEIGHT = 6
PIECES_PER_PLAYER = 7
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
        update_dominoes_sets(computer, computer.index(max_computer_double))
        return HUMAN
    else:
        update_dominoes_sets(human, human.index(max_human_double))
        return COMPUTER


def find_max_double_domino(pieces):
    doubles = []
    for piece in pieces:
        if piece[0] == piece[1]:
            doubles.append(piece)
    return [] if len(doubles) == 0 else max(doubles)


def has_double_dominoes(domino_set):
    for piece in domino_set:
        if piece[0] == piece[1]:
            return True
    return False


def move(player: str, dominoes: list):
    if player == COMPUTER:
        input('Status: Computer is about to make a move. Press Enter to continue...')
        piece = random.choice(dominoes)
        # TODO потом исправить +1. Это все из-за дурацкого условия про пропуск хода
        update_dominoes_sets(dominoes, dominoes.index(piece) + 1)
        return HUMAN
    if player == HUMAN:
        while True:
            try:
                domino_number = int(input("Status: It's your turn to make a move. Enter your command."))
            except ValueError:
                print('Invalid input. Please try again.')
                continue

            if abs(domino_number) > len(dominoes):
                print('Invalid input. Please try again.')
                continue

            update_dominoes_sets(dominoes, domino_number)
            break
        return COMPUTER


def update_dominoes_sets(player_set, domino_number):
    """
    To make a move, the player has to specify the action they want to take.
    In this project, the actions are represented by integer numbers in the following manner:
    {side_of_the_snake (+/-), domino_number (integer)} or {0}.
    For example:
        -6 : Take the sixth domino and place it on the left side of the snake.
        6 : Take the sixth domino and place it on the right side of the snake.
        0 : Take an extra piece from the stock (if it's not empty) and
        skip a turn or simply skip a turn if the stock is already empty by this point.
    """
    if domino_number == 0:
        if len(snake) != 0:
            index = random.choice(stock)
            player_set.append(index)
            stock.remove(index)
        return

    # жесть какая-то, а не условие
    if domino_number < 0:
        domino_number = abs(domino_number)
        domino_number -= 1
        snake.insert(0, player_set[domino_number])
    else:
        domino_number -= 1
        snake.append(player_set[domino_number])
    player_set.remove(player_set[domino_number])


def print_status(stock, players):
    print('=' * 70)
    # print(f'Stock size: {len(stock)}')
    print(f'Stock size: {stock}')
    # print(f'Computer pieces: {len(players[COMPUTER])}\n')
    print(f'Computer pieces: {players[COMPUTER]}\n')
    print(*snake)
    print(f'\nYour pieces:')
    for i, p in enumerate(players[HUMAN]):
        print(f'{i + 1}: {p}')


def play():
    global stock
    """
    Domino piece is double if the two numbers written on it are equal
    If no one has a double domino, the pieces are reshuffled and redistributed.
    """
    while True:
        stock = generate_domino_set()
        players = {COMPUTER: draw(),
                   HUMAN: draw()}
        if has_double_dominoes(players[COMPUTER]) or has_double_dominoes(players[HUMAN]):
            break

    next_player = start(players)

    while True:
        print_status(stock, players)
        next_player = move(next_player, players[next_player])

        if len(players[next_player]) == 0:
            break


if __name__ == '__main__':
    play()
