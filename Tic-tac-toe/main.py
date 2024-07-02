import sys
import pygame
import numpy as np

pygame.init()

#colors
WHITE = (255,255,255)
GRAY = (180, 180,180)
RED = (255,0,0)
GREEN = (0, 255,0)
BLACK = (0,0,0)

#proptions & sizes
WIDTH = 400
HEIGHT = 400
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH =25

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic TacToe game')
screen.fill(BLACK)

board = np.zeros((BOARD_ROWS, BOARD_COLS))

def draw_lines(color = WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0 , SQUARE_SIZE*i), (WIDTH, SQUARE_SIZE*i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE*i, 0), (SQUARE_SIZE*i, HEIGHT), LINE_WIDTH)


def dreaw_fig(color= WHITE):
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, color, (int(SQUARE_SIZE*c + SQUARE_SIZE//2),int(SQUARE_SIZE*r + SQUARE_SIZE//2)), CIRCLE_RADIUS, CIRCLE_WIDTH)

            elif board[r][c] == 2:
                pygame.draw.line(screen, color, (SQUARE_SIZE*c + SQUARE_SIZE//4, r*SQUARE_SIZE + SQUARE_SIZE//4), (c*SQUARE_SIZE + 3*SQUARE_SIZE//4, r*SQUARE_SIZE + 3 * SQUARE_SIZE//4), CROSS_WIDTH)
                pygame.draw.line(screen, color, (SQUARE_SIZE*c + SQUARE_SIZE//4, r*SQUARE_SIZE + 3*SQUARE_SIZE//4), (c*SQUARE_SIZE + 3*SQUARE_SIZE//4, r*SQUARE_SIZE + SQUARE_SIZE//4), CROSS_WIDTH)


def mark_sq(row, col, player):
    board[row][col] = player


def available_sq(row, col):
    return board[row][col] == 0


def is_board_full(check_board = board):
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if check_board[r][c] == 0:
                return False
            
    return True

def check_win(player, check_board =board):
    for c in range(BOARD_COLS):
        if check_board[0][c] == player and check_board[1][c] == player and check_board[2][c] == player:
            return True
        
    for r in range(BOARD_ROWS):
        if check_board[r][0] == player and check_board[r][1] == player and check_board[r][2] == player:
            return True

    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    
    return False


def minimax(minimax_board, depth, is_maximizing):
    if check_win(2, minimax_board):
        return float('inf')
    elif check_win(1, minimax_board):
        return float('-inf')
    elif is_board_full(minimax_board):
        return 0

    if is_maximizing:
        best_secore = -1000
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if minimax_board[r][c] == 0:
                    minimax_board[r][c] = 2
                    secore = minimax(minimax_board, depth + 1, False)
                    minimax_board[r][c] = 0
                    best_secore = max(best_secore, secore)
        
        return best_secore
    else:
        best_secore = 1000
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if minimax_board[r][c] == 0:
                    minimax_board[r][c] = 1
                    secore = minimax(minimax_board, depth + 1, True)
                    minimax_board[r][c] = 0
                    best_secore = min(best_secore, secore)
        
        return best_secore


def best_move():
    best_score = -1000
    move = (-1, -1)
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if board[r][c] == 0:
                board[r][c] = 2
                score = minimax(board, 0, False)
                board[r][c] = 0
                if score > best_score:
                    best_score = score
                    move = (r, c)
    
    if move != (-1,-1):
        mark_sq(move[0], move[1], 2)
        return True
    return False


def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            board[r][c] = 0


draw_lines()
player =1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE

            if available_sq(mouseY, mouseX):
                mark_sq(mouseY, mouseX, player)
                if check_win(player):
                    game_over = True
                player = player % 2 + 1

                if not game_over:
                    if best_move():
                        if check_win(2):
                            game_over = True
                        player = player % 2 + 1

                if not game_over:
                    if is_board_full():
                        game_over = True


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1

    if not game_over:
        dreaw_fig()
    else:
        if check_win(1):
            dreaw_fig(GREEN)
            draw_lines(GREEN)
        elif check_win(2):
            dreaw_fig(RED)
            draw_lines(RED)
        else:
            dreaw_fig(GRAY)
            draw_lines(GRAY)

    pygame.display.update()
