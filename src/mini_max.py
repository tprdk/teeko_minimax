import numpy as np
import copy

ROW = 5
COL = 5
INF = 100000000


moves = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1)
]


class MiniMax:
    def __init__(self, board=np.zeros(shape=(5, 5), dtype='int'), value=0):
        self.children = []
        self.value = value
        self.board = board


def print_board(board):
    for i in range(5):
        for j in range(5):
            print(f'{board[i][j]:>2}', end=' ')
        print()
    print()

def game_over(board):
    player_vertical_score = check_vertically(board, 1)
    ai_vertical_score = check_vertically(board, -1)

    player_horizontal_score = check_horizontally(board, 1)
    ai_horizontal_score = check_horizontally(board, -1)

    player_diagonally_score = check_diagonally(board, 1)
    ai_diagonally_score = check_diagonally(board, -1)

    if max(player_vertical_score, player_horizontal_score, player_diagonally_score) == 4:
        print('player won')
        return True
    elif max(ai_diagonally_score, ai_vertical_score, ai_horizontal_score) == 4:
        print('ai won')
        return True
    else:
        return False


def ai_insert_piece(player_pieces, ai_pieces):
    current_board = get_current_board_state(player_pieces, ai_pieces, piece_insert_phase=True)
    minimax = MiniMax(current_board)


def make_move(player_pieces, ai_pieces):
    current_board = get_current_board_state(player_pieces, ai_pieces)
    minimax = MiniMax(current_board)
    create_child_positions(minimax, 4, -1, True)
    minimax.value = create_minimax_tree(minimax, 4, -INF, INF, True)
    board = get_move(minimax)

    before, after = board_diff(minimax.board, board)
    before = (before[1] * 200, before[0] * 200)
    after = (after[1] * 200, after[0] * 200)
    return before, after

def create_child_positions(node, current_depth, target, backtrack):
    if current_depth != 0 and not game_over(node.board):
        node.children = check_all_valid_moves(node, target)
        for child in node.children:
            create_child_positions(child, current_depth - 1, target * -1, not backtrack)


def create_minimax_tree(node, current_depth, alpha, beta, maximize):
    if current_depth == 0 or game_over(node.board):
        return calculate_heuristic(node.board)
    if maximize:
        max_score = -INF
        for child in node.children:
            child.value = create_minimax_tree(child, current_depth - 1, alpha, beta, False)
            max_score = max(max_score, child.value)
            alpha = max(alpha, child.value)
            if beta <= alpha:
                break
        return max_score
    else:
        min_score = INF
        for child in node.children:
            child.value = create_minimax_tree(child, current_depth - 1, alpha, beta, True)
            min_score = min(min_score, child.value)
            beta = min(child.value, beta)
            if beta <= alpha:
                break
        return min_score


def board_diff(original_board, board):
    before = (-1, -1)
    after  = (-1, -1)
    #nt('\nselected board\n')
    #print_board(board)
    for i in range(5):
        for j in range(5):
            if original_board[i][j] != board[i][j]:
                if board[i][j] == 0:
                    before = (i, j)
                else:
                    after = (i, j)
    return before, after


def get_move(node):
    for child in node.children:
        print(f'parent  : {node.value} - child : {child.value}')
    for child in node.children:
        if child.value == node.value:
            return child.board


def get_current_board_state(player_pieces, ai_pieces, piece_insert_phase=False):
    board = np.zeros(shape=(5, 5), dtype='int')
    for player, ai in zip(player_pieces, ai_pieces):
        p_x_pos = int(player.y_pos / 200)
        p_y_pos = int(player.x_pos / 200)
        a_x_pos = int(ai.y_pos / 200)
        a_y_pos = int(ai.x_pos / 200)
        if piece_insert_phase:
            board[p_x_pos][p_y_pos] = 1
            board[a_x_pos][a_y_pos] = -1
        else:
            if player.inserted:
                board[p_x_pos][p_y_pos] = 1
            if ai.inserted:
                board[a_x_pos][a_y_pos] = -1
    return board


def valid_move(board, x_pos, y_pos, x, y):
    if 0 <= x_pos + x < 5 and 0 <= y_pos + y < 5 and board[x_pos + x][y_pos + y] == 0:
        return True
    return False


def check_all_valid_moves(node, target):
    pieces = np.argwhere(node.board == target)
    children = []
    for piece in pieces:
        for move in moves:
            x_pos = piece[0]
            y_pos = piece[1]
            if valid_move(node.board, x_pos, y_pos, move[0], move[1]):
                new_board = copy.deepcopy(node.board)
                new_board[x_pos][y_pos] = 0
                new_board[x_pos + move[0]][y_pos + move[1]] = target
                children.append(MiniMax(new_board))
    return children


def check_vertically(board, target):
    # black piece occurrences  for each row
    max_score = 0
    for i in range(5):
        j = 0
        t = 1
        occurrences = 1
        while j < 5:
            while j + t < 5 and board[i][j] == target and board[i][j] == board[i][j + t]:
                occurrences += 1
                t += 1
            max_score = max(max_score, occurrences)
            occurrences = 1
            t = 1
            j += 1
    return max_score


def check_horizontally(board, target):
    # black piece occurrences  for each col
    max_score = 0
    for i in range(5):
        j = 0
        t = 1
        occurrences = 1
        while j < 5:
            while j + t < 5 and board[j][i] == target and board[j][i] == board[j + t][i]:
                occurrences += 1
                t += 1
            max_score = max(max_score, occurrences)
            occurrences = 1
            t = 1
            j += 1
    return max_score


def diagonally_reverse(board, target, i):
    max_occurrences = 0
    occurrences = 0
    j = 0
    while j < 5:
        t = 1
        while 4 >= j - t >= 0 and 4 >= i + t >= 0 and board[i][j] == target and board[i][j] == board[i + t][j - t]:
            occurrences += 1
            t += 1
        if occurrences != 0:
            max_occurrences = max(max_occurrences, occurrences + 1)
            occurrences = 0
        j += 1
    return max_occurrences


def diagonally(board, target, i):
    max_occurrences = 0
    occurrences = 0
    j = 0
    while j < 4:
        t = 1
        while 0 <= j + t <= 4 and 4 >= i + t >= 0 and board[i][j] == target and board[i][j] == board[i + t][j + t]:
            occurrences += 1
            t += 1
        if occurrences != 0:
            max_occurrences = max(max_occurrences, occurrences + 1)
            occurrences = 0
        j += 1
    return max_occurrences


def check_diagonally(board, target):
    max_score = 0
    for i in range(ROW):
        occurrences = diagonally(board, target, i)
        occurrences_2 = diagonally_reverse(board, target, i)
        max_score = max(max_score, occurrences, occurrences_2)
    #print(f'diagonal score : {max_score}')
    return max_score


def calculate_heuristic(board):
    max_ai_score = max(check_vertically(board, -1), check_horizontally(board, -1), check_diagonally(board, -1))
    max_player_score = max(check_vertically(board, 1), check_horizontally(board, 1), check_diagonally(board, 1))
    if max_player_score == 4:
        return -4
    if max_ai_score == 4:
        return 4
    return max_ai_score - max_player_score
