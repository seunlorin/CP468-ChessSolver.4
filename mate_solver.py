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
        # Base case: when depth = 0 then return score
        if depth == 0:
            return self.evaluate_position(board), None

        # Check for checkmate for current side
        if board.is_checkmate():
            # If the current side is the maximizing player then White loses resulting in a negative number.
            if is_maximizing_player:
                return -100000, None
            # Otherwise White wins and returns a positive
            else:
                return 100000, None
            # Check for stalement, if there is then return 0
        if board.is_stalemate():
            return 0, None

        # Generate a list of all legal moves available
        legal_moves = list(board.legal_moves)
        # If there are no legal moves then there is a draw
        # If not caught in board.is_stalemate() then will be caught here
        if not legal_moves:
            return 0, None

        # Check for the maximizing player (White)
        if is_maximizing_player:
            max_eval = -float("inf") # Start with lowest score possible
            best_move = None
            # Try every legal move possible
            for move in legal_moves:
                board.push(move) # Make the move
                # Recursively search and get the resulting eval_score
                eval_score, _ = self.minimax_alpha_beta_search(
                    board, depth - 1, alpha, beta, False
                )
                board.pop() # Undo move to try next move

                # Keep the move if it gives a better score
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move

                alpha = max(alpha, max_eval) # Update alpha (best score so far for the maximizer)
                
                # Check for alpha-beta prune
                if beta <= alpha:
                    break

            return max_eval, best_move

        # Check for minimizing player (Black)
        # Essentially same as above but for a lower score
        else:
            min_eval = float("inf") # Start with highest score possible
            best_move = None

            for move in legal_moves:
                board.push(move)
                eval_score, _ = self.minimax_alpha_beta_search(
                    board, depth - 1, alpha, beta, True
                )
                board.pop()

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move

                beta = min(beta, min_eval)
                if beta <= alpha:
                    break

            return min_eval, best_move

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