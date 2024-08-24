import argparse
import chess
import chess.svg
import json
import os
import random

from PIL import Image, ImageDraw, ImageFont

# command Line
parser = argparse.ArgumentParser(description="Python App Configuration")
parser.add_argument(
    '--env', 
    type=str, choices=['development', 'staging', 'production'],
    help='Environment to use', required=True
    )
args = parser.parse_args()

# static variables
CONFIG_FOLDER = "./configs/"
ENV = args.env

# load configuration
with open(os.path.join(CONFIG_FOLDER, "config.json"), "r") as config_file:
    config = json.load(config_file)

# application variables
CHESS_PIECES_ASSETS_DIRECTORY = config[ENV]["CHESS_PIECES_ASSETS_DIRECTORY"]
CHESS_FEN_DATASET_FILENAME = config[ENV]["CHESS_FEN_DATASET_FILENAME"]
CHESS_PUZZLE_FILENAME = config[ENV]["CHESS_PUZZLE_FILENAME"]
CHESS_SQUARE_SIZE = config[ENV]["CHESS_SQUARE_SIZE"]
_ID, FEN, MOVES, RATING, RATING_DEVIATION, THEMES = 0, 1, 2, 3, 4, 7

pieces = {
    'P': Image.open(f"{CHESS_PIECES_ASSETS_DIRECTORY}/pawn-white.png"), 'N': Image.open(f"{CHESS_PIECES_ASSETS_DIRECTORY}/knight-white.png"), 
    'B': Image.open(f"{CHESS_PIECES_ASSETS_DIRECTORY}/bishop-white.png"), 'R': Image.open(f"{CHESS_PIECES_ASSETS_DIRECTORY}/rook-white.png"), 
    'Q': Image.open(f"{CHESS_PIECES_ASSETS_DIRECTORY}/queen-white.png"), 'K': Image.open(f"{CHESS_PIECES_ASSETS_DIRECTORY}/king-white.png"),
    'p': Image.open(f"{CHESS_PIECES_ASSETS_DIRECTORY}/pawn-black.png"), 'n': Image.open(f"{CHESS_PIECES_ASSETS_DIRECTORY}/knight-black.png"), 
    'b': Image.open(f"{CHESS_PIECES_ASSETS_DIRECTORY}/bishop-black.png"), 'r': Image.open(f"{CHESS_PIECES_ASSETS_DIRECTORY}/rook-black.png"), 
    'q': Image.open(f"{CHESS_PIECES_ASSETS_DIRECTORY}/queen-black.png"), 'k': Image.open(f"{CHESS_PIECES_ASSETS_DIRECTORY}/king-black.png")
}
for piece in pieces:
    pieces[piece] = pieces[piece].resize((CHESS_SQUARE_SIZE, CHESS_SQUARE_SIZE))

# load data
with open(CHESS_FEN_DATASET_FILENAME, "r") as dataset:
    chess_puzzle_list = dataset.readlines()

puzzle = random.choice(chess_puzzle_list[1:]).split(",")

def _draw_chessboard():
    board_size = 8 * CHESS_SQUARE_SIZE
    image = Image.new('RGB', (board_size, board_size), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    light_color = (240, 217, 181)  # Light square color
    dark_color = (181, 136, 99)    # Dark square color
    
    for i in range(8):
        for j in range(8):
            color = light_color if (i + j) % 2 == 0 else dark_color
            draw.rectangle([i * CHESS_SQUARE_SIZE, j * CHESS_SQUARE_SIZE, (i + 1) * CHESS_SQUARE_SIZE, (j + 1) * CHESS_SQUARE_SIZE], fill=color)

    return image

def _draw_piece_in_chessboard(piece, square, image):
    piece_symbol = piece.symbol()
    
    # Calculate the position of the piece on the image
    x = chess.square_file(square) * CHESS_SQUARE_SIZE
    y = (7 - chess.square_rank(square)) * CHESS_SQUARE_SIZE
    
    # Draw the piece
    piece_image = pieces[piece_symbol]
    piece_width, piece_height = piece_image.size
    centered_x = x + (CHESS_SQUARE_SIZE - piece_width) // 2
    centered_y = y + (CHESS_SQUARE_SIZE - piece_height) // 2
    image.paste(piece_image, (centered_x, centered_y), piece_image)

def flash(fen: str, filename: str):

    image, board = _draw_chessboard(), chess.Board(fen)
    board.push_uci(puzzle[MOVES].split(" ")[0])
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            _draw_piece_in_chessboard(piece, square, image)
            
    
    print(f"""
    PUZZLE: '{puzzle[_ID]}'
    
    \t'{"White" if board.turn else "Black"} to move' 
    
    FEN: {puzzle[FEN]}
    THEMES: '{puzzle[THEMES]}'
    SOLUTION: {puzzle[MOVES].split(" ")[1]}
    RATING: {puzzle[RATING]} RATING DEVIATION: {puzzle[RATING_DEVIATION]}
    """)

    # Save the image to a file
    image.save(filename)
    print(f"Chess board saved as '{filename}'.")

if __name__ == '__main__':

    fen, filename = puzzle[FEN], CHESS_PUZZLE_FILENAME
    flash(fen, filename)




