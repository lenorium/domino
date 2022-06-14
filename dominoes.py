import random

MIN_WEIGHT = 0
MAX_WEIGHT = 6
PIECES_PER_PLAYER = 7


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


def get_start_piece(player1, player2):
    max_double = [MAX_WEIGHT, MAX_WEIGHT]

    if max_double in player1 or max_double in player2:
        return max_double

    player1 = find_double_dominoes(player1)
    player2 = find_double_dominoes(player2)

    if len(player1) == 0:
        return max(player2)
    elif len(player2) == 0:
        return max(player1)
    else:
        return max(max(player1), max(player2))
    

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


def go(player, piece, snake: list):
    snake.append(piece)
    player.remove(piece)


def play():
    snake = []
    # Domino piece is double if the two numbers written on it are equal
    # If no one has a double domino, the pieces are reshuffled and redistributed.
    while True:
        stock = generate_domino_set()
        computer = draw(stock)
        human = draw(stock)
        if has_double_dominoes(computer) or has_double_dominoes(human):
            break

    # To start the game, players determine the starting piece.
    # The player with the highest double ([6,6] or [5,5] for example)
    # will donate that domino as a starting piece for the game.
    # After doing so, their opponent will start the game by going first.
    # --- ну такое ----
    init_piece = get_start_piece(computer, human)
    if init_piece in computer:
        init_player = computer
        first_player = human
    else:
        init_player = human
        first_player = computer
    go(init_player, init_piece, snake)
    #  --------------------------

    print(f'Stock pieces: {stock}')
    print(f'Computer pieces: {computer}')
    print(f'Player pieces: {human}')
    print(f'Domino snake: {snake}')
    # TODO исправить потом '!='
    print(f'Status: {"computer" if first_player == computer else "player"}')


if __name__ == '__main__':
    play()
