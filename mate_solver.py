"""
mate_solver.py

Initial Mate Solver scaffold for the term project.

This file provides:
- `MateSolver` class that can initialize a `chess.Board` from a FEN string.
- `evaluate_position(board)` placeholder that returns large scores for checkmate states.
- `minimax_alpha_beta_search(board, depth, alpha, beta, is_maximizing_player)` recursive
  signature with comments marking the base case, maximizing/minimizing loops, and alpha-beta
  pruning cut locations.

Uses the `python-chess` library for all rules and move generation.

References:
- https://www.chessprogramming.org/Main_Page
"""

import chess
import math 

class MateSolver:
    def __init__(self, fen_string=None):
        # Define score constants for checkmate and draw states
        self.MATE_SCORE = 100000 
        self.STALEMATE_SCORE = 0
        # Load the board, using the standard starting FEN if non is provided
        if fen_string:
            self.board = chess.Board(fen_string)
        else:
            self.board = chess.Board()
    
    # The recursive search function will go here 
    def minimax_alpha_beta_search(self, board, depth, alpha, beta, is_maximizing_player):
        # Base case: check for terminal states (checkmate, stalemate, draw) or depth limit
        pass 

    def evaluate_position(self, board):
        #1. Check for Terminal Game States:
        
        # Checkmate is a guaranteed win.
        if board.is_checkmate():
            # If it's Black's turn (chess.BLACK), White just checkmated Black.
            if board.turn == chess.BLACK:
                return self.MATE_SCORE # White wins (Maximizing Player)
            else:
                return -self.MATE_SCORE # Black wins (Minimizing Player)

        # Stalemate is a draw.
        if board.is_stalemate():
            return self.STALEMATE_SCORE
            
        # 2. Non-Terminal States: (Will be filled with material evaluation later)
        return 0 

# Test code
if __name__ == "__main__":
    # Example Mate in 1 puzzle FEN (White to move and mate)
    mate_in_1_fen = "8/R7/5K2/8/8/8/7r/7k w - - 0 1" 
    solver = MateSolver(mate_in_1_fen)
    print(solver.board)
    print(f"Is Checkmate? {solver.board.is_checkmate()}")





else:

    print("testing done here")