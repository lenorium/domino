import random

MIN_WEIGHT = 0
MAX_WEIGHT = 6
TILES_PER_PLAYER = 7
END_GAME_COUNTER = 8
COMPUTER = 'computer'
HUMAN = 'human'

MSG_COMPUTERS_TURN = 'Status: Computer is about to make a move. Press Enter to continue...\n'
MSG_HUMANS_TURN = "Status: It's your turn to make a move. Enter your command."
MSG_GAME_OVER_DRAW = "Status: The game is over. It's a draw!"
MSG_GAME_OVER_WIN = 'Status: The game is over. {0} won!'
MSG_INVALID_INPUT = 'Invalid input. Please try again.'
MSG_ILLEGAL_MOVE = 'Illegal move. Please try again.'

snake = []
stock = []


def prepare_stock():
    for i in range(MIN_WEIGHT, MAX_WEIGHT + 1):
        for j in range(i, MAX_WEIGHT + 1):
            stock.append([i, j])
    random.shuffle(stock)
    return stock


def draw():
    reserved = random.sample(stock, TILES_PER_PLAYER)
    for tile in reserved:
        stock.remove(tile)
    return reserved


def start(players):
    """
    To start the game, players determine the starting tile.
    The player with the highest double ([6,6] or [5,5] for example)
    will donate that domino as a starting tile for the game.
    After doing so, their opponent will start the game by going first.
    """
    computer = players[COMPUTER]
    human = players[HUMAN]

    max_computer_double = find_max_double(computer)
    max_human_double = find_max_double(human)

    if max_computer_double > max_human_double:
        update(computer, max_computer_double)
        return HUMAN
    else:
        update(human, max_human_double)
        return COMPUTER


def find_max_double(tiles):
    doubles = []
    for tile in tiles:
        if tile[0] == tile[1]:
            doubles.append(tile)
    return [] if len(doubles) == 0 else max(doubles)


def has_doubles(domino_set):
    return any(tile[0] == tile[1] for tile in domino_set)


def move(player: str, dominoes: list):
    chosen_tile = None
    if player == COMPUTER:
        next_player = HUMAN
        input(MSG_COMPUTERS_TURN)
        matching = get_matching_tiles(dominoes)
        if len(matching) == 1:
            chosen_tile = matching[0]
        elif len(matching) > 1:
            scores = get_score_per_num(matching)
            score_per_tile = get_score_per_tile(scores, matching)
            max_tile_index = max_score_tile(score_per_tile)
            chosen_tile = dominoes[max_tile_index]
    else:
        next_player = COMPUTER
        print(MSG_HUMANS_TURN)
        while True:
            try:
                index = abs(int(input())) - 1
            except ValueError:
                print(MSG_INVALID_INPUT)
                continue

            # if index == -1 then skip a turn
            if index == -1:
                break

            if index >= len(dominoes):
                print(MSG_INVALID_INPUT)
                continue

            chosen_tile = dominoes[index]
            if is_correct_tile(chosen_tile):
                break
            else:
                print(MSG_ILLEGAL_MOVE)
                continue

    left_side = False
    if chosen_tile is not None:
        left_side = is_to_left_side(chosen_tile)
        reverse_tile(chosen_tile, left_side)
    update(dominoes, chosen_tile, left_side)
    return next_player


def get_score_per_num(tiles):
    score = {i: 0 for i in range(MAX_WEIGHT + 1)}
    score = get_score_by_set(tiles, score)
    score = get_score_by_set(snake, score)
    return score


def get_score_per_tile(scores: dict, tiles):
    scores_by_tiles = {i: 0 for i in range(len(tiles))}
    for i in range(len(tiles)):
        for num in tiles[i]:
            scores_by_tiles[i] += scores.get(num)
    return scores_by_tiles


def max_score_tile(scores_by_tile):
    return max(scores_by_tile, key=scores_by_tile.get)


def get_score_by_set(tiles, score):
    for tile in tiles:
        for num in tile:
            score[num] += 1
    return score


def is_to_left_side(tile):
    return snake[-1][-1] not in tile


def get_matching_tiles(tiles):
    return list(filter(is_correct_tile, tiles))


def is_correct_tile(tile):
    return any(num == snake[0][0] or num == snake[-1][-1] for num in tile)


def reverse_tile(tile: list, left_side: bool):
    if left_side and tile[0] == snake[0][0] or not left_side and tile[-1] == snake[-1][-1]:
        tile.reverse()


def update(player_set, tile=None, left_side=False):
    # skip a turn
    if tile is None:
        if len(stock) != 0:
            index = random.choice(stock)
            player_set.append(index)
            stock.remove(index)
        return

    if left_side:
        snake.insert(0, tile)
    else:
        snake.append(tile)
    player_set.remove(tile)


def print_status(players):
    print('=' * 70)
    print(f'Stock size: {len(stock)}')
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


def is_over(players, player):
    """
    The end-game condition can be achieved in two ways:

    - One of the players runs out of tiles. The first player to do so is considered a winner.
    - The numbers on the ends of the snake are identical and appear within the snake 8 times. 
       For example, the snake below will satisfy this condition:
      [5,5],[5,2],[2,1],[1,5],[5,4],[4,0],[0,5],[5,3],[3,6],[6,5]
      These two snakes, however, will not:
      [5,5],[5,2],[2,1],[1,5],[5,4],[4,0],[0,5]
      [6,5],[5,5],[5,2],[2,1],[1,5],[5,4],[4,0],[0,5],[5,3],[3,1]
      If this condition is satisfied, it is no longer possible to go on with this snake.
      Even after emptying the stock, no player will have the necessary tile.
      Essentially, the game has come to a permanent stop, so we have a draw.
    """
    opponent = HUMAN if player == COMPUTER else COMPUTER
    if len(players[player]) > 0 \
            and len(get_matching_tiles(players[player])) == 0 \
            and len(stock) == 0 \
            and len(get_matching_tiles(players[opponent])) == 0:
        print(MSG_GAME_OVER_DRAW)
        return True

    if len(players[player]) == 0:
        print(MSG_GAME_OVER_WIN.format('The computer' if player == COMPUTER else 'You'))
        return True

    if snake[0][0] == snake[-1][-1] and \
            sum(num == snake[0][0] for tile in snake for num in tile) == END_GAME_COUNTER:
        print(MSG_GAME_OVER_DRAW)
        return True
    return False


def play():
    """
    Domino tile is double if the two numbers written on it are equal
    If no one has a double domino, the tiles are reshuffled and redistributed.
    """
    global stock
    while True:
        stock = prepare_stock()
        players = {COMPUTER: draw(), HUMAN: draw()}

        if has_doubles(players[COMPUTER]) or has_doubles(players[HUMAN]):
            break

    next_player = start(players)

    while not is_over(players, next_player):
        print_status(players)
        next_player = move(next_player, players[next_player])


if __name__ == '__main__':
    play()
