import numpy as np
import pygame
import sys
from Piece import Piece
from mini_max import make_move, game_over, get_current_board_state, ai_insert_piece

GREEN = (0, 150, 0)
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000
BLOCK_SIZE = 200
PIECE_COUNT = 4

RED_PIECE = pygame.image.load('../image/red_piece.png')
BLACK_PIECE = pygame.image.load('../image/black_piece.png')

def init_legal_squares():
    legal_squares = []
    for x in range(WINDOW_WIDTH // BLOCK_SIZE):
        for y in range(WINDOW_HEIGHT // BLOCK_SIZE):
            legal_squares.append(pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    return legal_squares

def draw_grid(screen, selected_square):
    for x in range(WINDOW_WIDTH // BLOCK_SIZE):
        for y in range(WINDOW_HEIGHT // BLOCK_SIZE):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 5)
    if selected_square[0] != -1:
        rect = pygame.Rect(selected_square[0], selected_square[1], BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, BLUE, rect, 5)

def draw_screen(screen, selected_square, player_pieces, ai_pieces):
    screen.fill(GREEN)
    draw_grid(screen, selected_square)
    for player, ai in zip(player_pieces, ai_pieces):
        if player.inserted:
            screen.blit(player.image, (player.x_pos, player.y_pos))
        if ai.inserted:
            screen.blit(ai.image, (ai.x_pos, ai.y_pos))
    pygame.display.update()

def check_mouse_collision(pieces, mouse_position, selected_square, collided):
    for piece in pieces:
        if piece.rect.collidepoint(mouse_position):
            selected_square = (piece.x_pos, piece.y_pos)
            piece.selected = True
            collided = True
        else:
            piece.selected = False
    return selected_square, collided

def valid_move(x_pos, y_pos, x_target, y_target):
    if np.sqrt((x_pos - x_target)**2 + (y_pos - y_target)**2) > 200 * np.sqrt(2):
        return False
    return True

def move_selected_piece(pieces, target_square, selected_square):
    for piece in pieces:
        if selected_square == (piece.x_pos, piece.y_pos):
            if valid_move(piece.x_pos, piece.y_pos, target_square[0], target_square[1]):
                piece.move(target_square[0], target_square[1])
            selected_square = (-1, -1)
    return selected_square

def insert_piece(piece, target_square):
    piece.inserted = True
    piece.move(target_square[0], target_square[1])

def check_all_pieces_inserted(pieces):
    i = 0
    while i < len(pieces):
        if not pieces[i].inserted:
            return False
        i += 1
    return True

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    legal_squares = init_legal_squares()

    player_pieces = []
    ai_pieces = []
    for i in range(PIECE_COUNT):
        player_pieces.append(Piece(pygame.transform.scale(RED_PIECE, (BLOCK_SIZE, BLOCK_SIZE))))
        ai_pieces.append(Piece(pygame.transform.scale(BLACK_PIECE, (BLOCK_SIZE, BLOCK_SIZE))))

    selected_square = (-1, -1)
    target_square = (-200, -200)
    insert_turn = True
    while not check_all_pieces_inserted(ai_pieces):
        draw_screen(screen, selected_square, player_pieces, ai_pieces)
        mouse_position = pygame.mouse.get_pos()
        if insert_turn:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for square in legal_squares:
                        if square.collidepoint(mouse_position):
                            target_square = (square.x, square.y)

                    for p in player_pieces:
                        if not p.inserted:
                            insert_piece(p, target_square)
                            break
                    insert_turn = False
        else:
            #ai part
            current, target = ai_insert_piece(player_pieces, ai_pieces)
            move_selected_piece(ai_pieces, target, current)
            insert_turn = True
            '''for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for square in legal_squares:
                        if square.collidepoint(mouse_position):
                            target_square = (square.x, square.y)
                    for p in ai_pieces:
                        if not p.inserted:
                            insert_piece(p, target_square)
                            break
                    insert_turn = True'''

    move_turn = True
    while not game_over(get_current_board_state(player_pieces, ai_pieces)):
        draw_screen(screen, selected_square, player_pieces, ai_pieces)
        if move_turn:
            mouse_position = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    collided = False
                    selected_square, collided = \
                        check_mouse_collision(player_pieces, mouse_position, selected_square, collided)
                    if not collided:
                        target_square = (0, 0)
                        for square in legal_squares:
                            if square.collidepoint(mouse_position):
                                target_square = (square.x, square.y)
                                move_turn = False
                        selected_square = move_selected_piece(player_pieces, target_square, selected_square)
        else:
            current, target = make_move(player_pieces, ai_pieces)
            move_selected_piece(ai_pieces, target, current)
            move_turn = True

    draw_screen(screen, selected_square, player_pieces, ai_pieces)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    main()