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
from typing import Optional
import chess


class MateSolver:
    """A simple mate searcher skeleton using python-chess.

    Notes:
    - This is an initial scaffold. The evaluation function is a placeholder and
      currently returns only mate scores. Material and positional evaluation
      will be added later.
    - The minimax search includes alpha-beta pruning and is written recursively.
    """

    def __init__(self, fen: Optional[str] = None) -> None:
        """Initialize the solver with an optional FEN. If no FEN provided, use the standard start position."""
        self.board = chess.Board(fen) if fen else chess.Board()

    def evaluate_position(self, board: chess.Board) -> int:
        """Non-recursive placeholder evaluation.

        Returns:
        - +100000 if White has just checkmated Black (very good for White).
        - -100000 if Black has just checkmated White (very bad for White).
        - 0 otherwise.

        Important: This function evaluates from White's perspective. A returned
        positive score means the position is winning for White.
        """
        # If the position is checkmate, the side to move is checkmated.
        # If it's Black to move and the position is checkmate, White delivered mate.
        if board.is_checkmate():
            if board.turn == chess.BLACK:
                # Black to move but is checkmated => White delivered mate
                return 100000
            else:
                # White to move but is checkmated => Black delivered mate
                return -100000

        # Placeholder: no other evaluation yet
        return 0

    def minimax_alpha_beta_search(self, board: chess.Board, depth: int, alpha: float, beta: float, is_maximizing_player: bool) -> float:
        """Recursive minimax search with alpha-beta pruning.

        Signature: (board, depth, alpha, beta, is_maximizing_player)

        The body below contains the full recursive call structure. The current
        implementation includes comments marking where the base case, the
        maximizing and minimizing loops, and alpha-beta pruning cuts occur.
        """

        # ---------- Base case ----------
        # Base case: depth == 0 or game over (checkmate/stalemate/insufficient material)
        # In the base case, evaluate the position and return the static score.
        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board)

        # ---------- Maximizing player ----------
        if is_maximizing_player:
            max_eval = -float("inf")
            # Maximizing loop: iterate over legal moves for the maximizing side
            for move in board.legal_moves:
                board.push(move)
                # Recurse as the minimizing player
                score = self.minimax_alpha_beta_search(board, depth - 1, alpha, beta, False)
                board.pop()

                if score > max_eval:
                    max_eval = score

                if score > alpha:
                    alpha = score

                # ---------- Alpha-Beta pruning cut (for maximizing) ----------
                # If alpha >= beta, we can prune remaining moves
                if beta <= alpha:
                    break

            return max_eval

        # ---------- Minimizing player ----------
        else:
            min_eval = float("inf")
            # Minimizing loop: iterate over legal moves for the minimizing side
            for move in board.legal_moves:
                board.push(move)
                # Recurse as the maximizing player
                score = self.minimax_alpha_beta_search(board, depth - 1, alpha, beta, True)
                board.pop()

                if score < min_eval:
                    min_eval = score

                if score < beta:
                    beta = score

                # ---------- Alpha-Beta pruning cut (for minimizing) ----------
                # If beta <= alpha, we can prune remaining moves
                if beta <= alpha:
                    break

            return min_eval


if __name__ == "__main__":
    # Small usage example. NOTE: Running a deep search from the initial
    # chess starting position will be very slow; this is just an example of
    # how to call the solver.
    solver = MateSolver()  # default starting position
    print("Starting position:")
    print(solver.board)

    # Example shallow search: depth=4 (plies), which corresponds to Mate in 2 searches
    score = solver.minimax_alpha_beta_search(solver.board, depth=4, alpha=-float('inf'), beta=float('inf'), is_maximizing_player=True)
    print("Shallow search score:", score)
