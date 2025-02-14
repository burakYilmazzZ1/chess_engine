import pygame
import sys
import copy
import time

pygame.init()

WIDTH = 1000  
HEIGHT = 800 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Satranç Oyunu')

ROWS = 8
COLS = 8
SQUARE_SIZE = 800 // COLS  


PROMOTION_MENU_HEIGHT = 120  
PIECE_SIZE = 40  
MENU_WIDTH = 4 * PIECE_SIZE 
MENU_X = (WIDTH - MENU_WIDTH) // 2  
MENU_Y = (HEIGHT - PROMOTION_MENU_HEIGHT) // 2 

LIGHT_GRAY = (230, 230, 230)  
WHITE = (255, 255, 255)  
BLACK = (0, 0, 0) 
TRANSPARENT_GRAY = (200, 200, 200, 128)  

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (205, 133, 63)
TAN = (222, 184, 135)
LIGHT_GRAY = (211, 211, 211)  

IMAGE_PATH = '/Users/burak.yilmaz/satranç/imag/'

def draw_board(screen):
    colors = [TAN, BROWN]
    for row in range(ROWS):
        for col in range(COLS):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def load_images(image_path):
    images = {}
    images['bP'] = pygame.transform.scale(
        pygame.image.load(f'{image_path}black pawn.png'), (SQUARE_SIZE, SQUARE_SIZE)
    )
    images['bR'] = pygame.transform.scale(
        pygame.image.load(f'{image_path}black rook.png'), (SQUARE_SIZE, SQUARE_SIZE)
    )
    images['bN'] = pygame.transform.scale(
        pygame.image.load(f'{image_path}black knight.png'), (SQUARE_SIZE, SQUARE_SIZE)
    )
    images['bB'] = pygame.transform.scale(
        pygame.image.load(f'{image_path}black bishop.png'), (SQUARE_SIZE, SQUARE_SIZE)
    )
    images['bQ'] = pygame.transform.scale(
        pygame.image.load(f'{image_path}black queen.png'), (SQUARE_SIZE, SQUARE_SIZE)
    )
    images['bK'] = pygame.transform.scale(
        pygame.image.load(f'{image_path}black king.png'), (SQUARE_SIZE, SQUARE_SIZE)
    )
    images['wP'] = pygame.transform.scale(
        pygame.image.load(f'{image_path}white pawn.png'), (SQUARE_SIZE, SQUARE_SIZE)
    )
    images['wR'] = pygame.transform.scale(
        pygame.image.load(f'{image_path}white rook.png'), (SQUARE_SIZE, SQUARE_SIZE)
    )
    images['wN'] = pygame.transform.scale(
        pygame.image.load(f'{image_path}white knight.png'), (SQUARE_SIZE, SQUARE_SIZE)
    )
    images['wB'] = pygame.transform.scale(
        pygame.image.load(f'{image_path}white bishop.png'), (SQUARE_SIZE, SQUARE_SIZE)
    )
    images['wQ'] = pygame.transform.scale(
        pygame.image.load(f'{image_path}white queen.png'), (SQUARE_SIZE, SQUARE_SIZE)
    )
    images['wK'] = pygame.transform.scale(
        pygame.image.load(f'{image_path}white king.png'), (SQUARE_SIZE, SQUARE_SIZE)
    )
    return images

def create_board():
    board = [
        ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
        ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
        ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
    ]
    return board

def draw_pieces(screen, board, images):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != 0:  
                piece_img = images.get(piece)  
                if piece_img:
                    screen.blit(piece_img, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    print(f"Resim bulunamadı: {piece}")  


def is_valid_move(board, start_pos, end_pos, player, en_passant_target=None):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    piece = board[start_row][start_col]

    if board[end_row][end_col] != 0 and board[end_row][end_col][0] == player:
        return False

    if piece[1] == 'P':
        is_legal = is_valid_pawn_move(board, start_pos, end_pos, player, en_passant_target)
    elif piece[1] == 'N':
        is_legal = is_valid_knight_move(board, start_pos, end_pos, player)
    elif piece[1] == 'R':
        is_legal = is_valid_rook_move(board, start_pos, end_pos, player)
    elif piece[1] == 'Q':
        is_legal = is_valid_queen_move(board, start_pos, end_pos, player)
    elif piece[1] == 'B':
        is_legal = is_valid_bishop_move(board, start_pos, end_pos, player)
    elif piece[1] == 'K':
        is_legal = is_valid_king_move(board, start_pos, end_pos, player)
    else:
        return False

    if not is_legal:
        return False

    board_copy = copy.deepcopy(board)  
    board_copy[end_row][end_col] = board_copy[start_row][start_col]  
    board_copy[start_row][start_col] = 0  

    if is_in_check(board_copy, player):
        return False

    return True

def is_stalemate(board, player):
    if is_in_check(board, player):
        return False  

    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] != 0 and board[row][col][0] == player:
                for r in range(ROWS):
                    for c in range(COLS):
                        if is_valid_move(board, (row, col), (r, c), player):
                            return False  

    return True  

position_history = {}

def update_position_history(board):
    global position_history
    position_str = str(board)
    if position_str in position_history:
        position_history[position_str] += 1
    else:
        position_history[position_str] = 1

def is_threefold_repetition():
    return any(count >= 3 for count in position_history.values())

half_move_clock = 0 

def reset_half_move_clock():
    global half_move_clock
    half_move_clock = 0

def increment_half_move_clock():
    global half_move_clock
    half_move_clock += 1

def is_fifty_move_rule():
    return half_move_clock >= 50

def is_insufficient_material(board):
    pieces = {'w': [], 'b': []}

    for row in board:
        for piece in row:
            if piece != 0:
                pieces[piece[0]].append(piece[1])

    for color in ['w', 'b']:
        if pieces[color] == ['K']:
            continue  

        if sorted(pieces[color]) in [['K', 'B'], ['K', 'N']]:  
            continue  

        return False  

    return True 


def is_checkmate(board, player):
    if not is_in_check(board, player):
        return False
    
    for row in range(8):
        for col in range(8):
            if board[row][col] != 0 and board[row][col][0] == player:
                for r in range(8):
                    for c in range(8):
                        if is_valid_move(board, (row, col), (r, c), player):
                            return False  
    return True

def is_in_check(board, player):

    king_pos = None

    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == f"{player}K":  
                king_pos = (row, col)
                break
        if king_pos:
            break  

    if king_pos is None:
        return False 
    return is_square_attacked(board, king_pos, player)


def is_valid_queen_move(board, start_pos, end_pos, player):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if board[end_row][end_col] != 0 and board[end_row][end_col][0] == player:
        return False

    if start_col == end_col:
        step = 1 if end_row > start_row else -1
        for row in range(start_row + step, end_row, step):
            if board[row][start_col] != 0:
                return False
        if board[end_row][end_col] != 0 and board[end_row][end_col][0] != player:
            return True
        return True

    if start_row == end_row:
        step = 1 if end_col > start_col else -1
        for col in range(start_col + step, end_col, step):
            if board[start_row][col] != 0:
                return False
        if board[end_row][end_col] != 0 and board[end_row][end_col][0] != player:
            return True
        return True

    if abs(start_row - end_row) == abs(start_col - end_col):
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        row, col = start_row + row_step, start_col + col_step
        while row != end_row and col != end_col:
            if board[row][col] != 0:
                return False
            row += row_step
            col += col_step
        if board[end_row][end_col] != 0 and board[end_row][end_col][0] != player:
            return True
        return True

    return False

def is_square_attacked(board, square, player):
    opponent = 'b' if player == 'w' else 'w'
    target_row, target_col = square

    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != 0 and piece[0] == opponent:
                
                if piece[1] == 'P':
                    pawn_attack_row = row + (1 if opponent == 'b' else -1)
                    if 0 <= pawn_attack_row < ROWS and 0 <= col - 1 < COLS:
                        if (pawn_attack_row, col - 1) == (target_row, target_col):
                            return True
                    if 0 <= pawn_attack_row < ROWS and 0 <= col + 1 < COLS:
                        if (pawn_attack_row, col + 1) == (target_row, target_col):
                            return True

                if piece[1] == 'R' and is_valid_rook_move(board, (row, col), square, opponent):
                    return True
                elif piece[1] == 'N' and is_valid_knight_move(board, (row, col), square, opponent):
                    return True
                elif piece[1] == 'B' and is_valid_bishop_move(board, (row, col), square, opponent):
                    return True
                elif piece[1] == 'Q' and is_valid_queen_move(board, (row, col), square, opponent):
                    return True
                elif piece[1] == 'K' and is_valid_king_move(board, (row, col), square, opponent, check_for_attack=True):
                    return True

    return False



def is_valid_pawn_move(board, start_pos, end_pos, player, en_passant_target):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    direction = -1 if player == 'w' else 1
    start_row_initial = 6 if player == 'w' else 1

    if start_col == end_col and board[end_row][end_col] == 0:
        if end_row - start_row == direction:
            return True
        if start_row == start_row_initial and end_row - start_row == 2 * direction and board[start_row + direction][start_col] == 0:
            return True

    if abs(start_col - end_col) == 1 and end_row - start_row == direction:
        if board[end_row][end_col] != 0 and board[end_row][end_col][0] != player:
            return True
        if (end_row, end_col) == en_passant_target:
            board[start_row][end_col] = 0
            return True

    return False

PROMOTION_MENU_HEIGHT = 120  
PIECE_SIZE = 40  
BUTTON_SIZE = 50  
BUTTON_SPACING = 10  

MENU_WIDTH = BUTTON_SIZE * 4 + BUTTON_SPACING * 3  
MENU_X = (WIDTH - MENU_WIDTH) // 2  
MENU_Y = (HEIGHT - PROMOTION_MENU_HEIGHT) // 2  

def draw_promotion_menu():

    pygame.draw.rect(SCREEN, LIGHT_GRAY, (MENU_X, MENU_Y, MENU_WIDTH, PROMOTION_MENU_HEIGHT))
    pygame.draw.rect(SCREEN, WHITE, (MENU_X, MENU_Y, MENU_WIDTH, PROMOTION_MENU_HEIGHT), 5)  # White border

def draw_piece_buttons(pieces, player):
    """Draw the piece buttons in the promotion menu at the center."""
    for i, piece in enumerate(pieces):
        piece_image = f"{player}{piece}"  
        
        x_pos = MENU_X + i * (BUTTON_SIZE + BUTTON_SPACING)  
        y_pos = MENU_Y + (PROMOTION_MENU_HEIGHT - BUTTON_SIZE) // 2  

        pygame.draw.rect(SCREEN, TRANSPARENT_GRAY, (x_pos, y_pos, BUTTON_SIZE, BUTTON_SIZE))  
        pygame.draw.rect(SCREEN, BLACK, (x_pos, y_pos, BUTTON_SIZE, BUTTON_SIZE), 2)  
        
        SCREEN.blit(load_images(IMAGE_PATH)[piece_image], (x_pos + (BUTTON_SIZE - PIECE_SIZE) // 2, y_pos + (BUTTON_SIZE - PIECE_SIZE) // 2))

def handle_click(pieces):
    selected_piece = None
    while selected_piece is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos[0], pos[1]

                if MENU_X <= x < MENU_X + MENU_WIDTH and MENU_Y <= y < MENU_Y + PROMOTION_MENU_HEIGHT:
                    index = (x - MENU_X) // (BUTTON_SIZE + BUTTON_SPACING)
                    if 0 <= index < len(pieces):
                        selected_piece = pieces[index]

        pygame.display.flip() 

    return selected_piece

def promote_pawn(board, row, col, player):
    pieces = ['R', 'N', 'B', 'Q'] 
    draw_promotion_menu()
    draw_piece_buttons(pieces, player)

    selected_piece = handle_click(pieces)

    board[row][col] = f"{player}{selected_piece}"
   
    return board  

def is_valid_rook_move(board, start_pos, end_pos, player):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if board[end_row][end_col] != 0 and board[end_row][end_col][0] == player:
        return False

    if start_col == end_col:
        step = 1 if end_row > start_row else -1
        for row in range(start_row + step, end_row, step):
            if board[row][start_col] != 0:
                return False
        return True

    if start_row == end_row:
        step = 1 if end_col > start_col else -1
        for col in range(start_col + step, end_col, step):
            if board[start_row][col] != 0:
                return False
        return True

    return False


def is_valid_bishop_move(board, start_pos, end_pos, player):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if abs(start_row - end_row) == abs(start_col - end_col):
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1

        current_row = start_row + row_step
        current_col = start_col + col_step

        while current_row != end_row and current_col != end_col:
            if board[current_row][current_col] != 0:
                return False  
            current_row += row_step
            current_col += col_step

        if board[end_row][end_col] == 0 or board[end_row][end_col][0] != player:
            return True

    return False

def is_valid_knight_move(board, start_pos, end_pos, player):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or \
       (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
        if board[end_row][end_col] == 0 or board[end_row][end_col][0] != player:
            return True
    return False



def create_board():
    board = [
        ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
        ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
        ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
    ]
    return board

def move_piece(board, start_pos, end_pos):

    start_row, start_col = start_pos
    end_row, end_col = end_pos
    piece = board[start_row][start_col]

    board[end_row][end_col] = piece
    board[start_row][start_col] = 0

    if piece == "wK":
        moved_flags["wK"] = True
    elif piece == "wR" and start_row == 7 and start_col == 7:
        moved_flags["wR_kingside"] = True
    elif piece == "wR" and start_row == 7 and start_col == 0:
        moved_flags["wR_queenside"] = True
    elif piece == "bK":
        moved_flags["bK"] = True
    elif piece == "bR" and start_row == 0 and start_col == 7:
        moved_flags["bR_kingside"] = True
    elif piece == "bR" and start_row == 0 and start_col == 0:
        moved_flags["bR_queenside"] = True

def promote_pawn(board, row, col, player):
    pieces = ['R', 'N', 'B', 'Q']  

    draw_promotion_menu()
    draw_piece_buttons(pieces, player)

    selected_piece = handle_click(pieces)

    board[row][col] = f"{player}{selected_piece}"

    if selected_piece == 'R':
        if player == 'w':
            if col == 0:
                moved_flags["wR_queenside"] = True
            elif col == 7:
                moved_flags["wR_kingside"] = True
        elif player == 'b':
            if col == 0:
                moved_flags["bR_queenside"] = True
            elif col == 7:
                moved_flags["bR_kingside"] = True

    return board  

moved_flags = {
    "wK": False,
    "bK": False,
    "wR_kingside": False,
    "wR_queenside": False,
    "bR_kingside": False,
    "bR_queenside": False
}

def can_castle(board, player, rook_col, target_cols, rook_flag):
    row = 7 if player == 'w' else 0
    king_piece = f"{player}K"
    
    if board[row][4] != king_piece or board[row][rook_col] != f"{player}R":
        return False
    if moved_flags[f"{player}K"] or moved_flags[rook_flag]:
        return False
    if any(board[row][col] != 0 for col in target_cols):
        return False
    if any(is_square_attacked(board, (row, col), player) for col in [4] + list(target_cols)):
        return False

    return True

def execute_castle(board, player, king_target, rook_start, rook_target):

    row = 7 if player == 'w' else 0
    king_piece = f"{player}K"
    rook_piece = f"{player}R"
    
    board[row][4] = 0  
    board[row][rook_start] = 0  
    board[row][king_target] = king_piece  
    board[row][rook_target] = rook_piece  

    moved_flags[f"{player}K"] = True
    if rook_start == 7:
        moved_flags[f"{player}R_kingside"] = True
    elif rook_start == 0:
        moved_flags[f"{player}R_queenside"] = True

def short_castle(board, player):
    if can_castle(board, player, 7, [5, 6], f"{player}R_kingside"):
        execute_castle(board, player, 6, 7, 5)
        return True
    return False

def long_castle(board, player):
    if can_castle(board, player, 0, [1, 2], f"{player}R_queenside"):
        execute_castle(board, player, 2, 0, 3)
        return True
    return False

def is_valid_king_move(board, start_pos, end_pos, player, check_for_attack=False):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if board[end_row][end_col] != 0 and board[end_row][end_col][0] == player:
        return False

    if not check_for_attack:
        if start_row == end_row and start_col == 4:
            
            if end_col == 6:
                return short_castle(board, player)
            
            elif end_col == 2:
                return long_castle(board, player)

    if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
        
        if not check_for_attack:
            if is_square_attacked(board, (end_row, end_col), player):
                return False
        return True

    return False



def draw_message(screen, message, position, color=(0, 0, 0), duration=1.5):
    font = pygame.font.Font(None, 40)  
    text = font.render(message, True, color)  
    text_rect = text.get_rect(midright=position)  
    
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    if message == "CHECK":
        return

    start_time = pygame.time.get_ticks() 
    while pygame.time.get_ticks() - start_time < duration * 1000:
        pygame.event.pump()  
        pygame.display.flip()  
    
    pygame.draw.rect(screen, (255, 255, 255), text_rect)  
    pygame.display.flip()  

def game_loop(screen, images):
    global half_move_clock, position_history  
    clock = pygame.time.Clock()
    board = create_board()
    running = True
    selected_piece = None
    player_turn = 'w'
    en_passant_target = None
    check_message = False
    checkmate_message = False
    draw_message_text = "continues..."
    draw_message_color = (255, 0, 0)

    position_history = {}  
    half_move_clock = 0  

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if (checkmate_message or draw_message_text != "continues...") and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                board = create_board()
                player_turn = 'w'
                checkmate_message = False
                check_message = False
                draw_message_text = "continues..."
                position_history = {}
                half_move_clock = 0

            if not checkmate_message and draw_message_text == "continues..." and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = pos[1] // SQUARE_SIZE

                if 0 <= row < ROWS and 0 <= col < COLS:
                    if selected_piece:
                        if is_valid_move(board, selected_piece, (row, col), player_turn, en_passant_target):
                            start_row, start_col = selected_piece
                            if board[start_row][start_col] != 0:
                                board[row][col] = board[start_row][start_col]
                                board[start_row][start_col] = 0

                            if board[row][col] != 0 and board[row][col][1] == 'P':
                                if (player_turn == 'w' and row == 0) or (player_turn == 'b' and row == 7):
                                    promote_pawn(board, row, col, player_turn)
                            
                            if board[row][col] != 0 and board[row][col][1] == 'P' and abs(row - selected_piece[0]) == 2:
                                en_passant_target = (row + (1 if player_turn == 'w' else -1), col)
                            else:
                                en_passant_target = None
                            
                            
                            if board[row][col][1] == 'P' or board[row][col] != 0:
                                reset_half_move_clock()
                            else:
                                increment_half_move_clock()
                            
                            
                            update_position_history(board)

                            player_turn = 'b' if player_turn == 'w' else 'w'
                            check_message = is_in_check(board, player_turn)

                            if is_checkmate(board, player_turn):
                                checkmate_message = True
                                draw_message_text = "CHECKMATE"
                                draw_message_color = (255, 0, 0)
                            elif is_stalemate(board, player_turn):
                                draw_message_text = "STALEMATE"
                                draw_message_color = (0, 0, 255)
                            elif is_threefold_repetition():
                                draw_message_text = "DRAW (Threefold Repetition)"
                                draw_message_color = (0, 0, 255)
                            elif is_fifty_move_rule():
                                draw_message_text = "DRAW (50-move rule)"
                                draw_message_color = (0, 0, 255)
                            elif is_insufficient_material(board):
                                draw_message_text = "DRAW (Insufficient Material)"
                                draw_message_color = (0, 0, 255)
                        
                        selected_piece = None
                    else:
                        if board[row][col] != 0 and board[row][col][0] == player_turn:
                            selected_piece = (row, col)

        draw_board(screen)
        draw_pieces(screen, board, images)
        draw_message(screen, "CHECK", (980, 500), color=(0, 0, 0))
        if checkmate_message:
            draw_message(screen, "CHECK", (980, 500), color=(0, 0, 0))
            draw_message(screen, "CHECKMATE", (980, 400), color=(255, 0, 0))
            draw_message(screen, "Press ENTER to restart", (980, 450), color=(0, 255, 0))
        elif draw_message_text != "continues...":
            draw_message(screen, "CHECK", (980, 500), color=(0, 0, 0))
            draw_message(screen, draw_message_text, (980, 400), color=draw_message_color)
            draw_message(screen, "Press ENTER to restart", (980, 450), color=(0, 255, 0))
        elif check_message:
            draw_message(screen, "CHECK", (980, 500), color=(255, 0, 0))

        pygame.display.flip()
        clock.tick(60)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")
    
    images = load_images(IMAGE_PATH)  
    game_loop(screen, images)
    
    pygame.quit()

if __name__ == "__main__":
    main()