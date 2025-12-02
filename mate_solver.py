import tkinter as tk
import chess
import math

# ---------- Mate Solver ----------
class MateSolver:
    def __init__(self, fen_string=None):
        self.MATE_SCORE = 100000
        self.STALEMATE_SCORE = 0
        self.board = chess.Board(fen_string) if fen_string else chess.Board()
        self.search_depth = 4  # default depth in plies

    def set_search_depth(self, depth):
        """Set search depth in plies (half-moves)"""
        self.search_depth = depth

    def evaluate_position(self, board, depth):
        """Evaluate board position. High positive = White winning, High negative = Black winning"""
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                return -self.MATE_SCORE + depth  # Black delivered mate
            else:
                return self.MATE_SCORE - depth   # White delivered mate
        if board.is_stalemate():
            return 0

        # Material evaluation for non-terminal positions
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 300,
            chess.BISHOP: 300,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 0
        }

        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                score += value if piece.color == chess.WHITE else -value
        return score

    def minimax_alpha_beta_search(self, board, depth=None, alpha=-math.inf, beta=math.inf):
        if depth is None:
            depth = self.search_depth

        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board, depth), None

        maximizing = board.turn == chess.WHITE
        best_move = None

        if maximizing:
            max_eval = -math.inf
            for move in board.legal_moves:
                board.push(move)
                eval_score, _ = self.minimax_alpha_beta_search(board, depth - 1, alpha, beta)
                board.pop()
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in board.legal_moves:
                board.push(move)
                eval_score, _ = self.minimax_alpha_beta_search(board, depth - 1, alpha, beta)
                board.pop()
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_mate_sequence(self):
        """Return the sequence of moves leading to mate, using the search_depth"""
        sequence = []
        temp_board = self.board.copy()

        for move_num in range(self.search_depth):
            remaining_depth = self.search_depth - move_num
            score, move = self.minimax_alpha_beta_search(temp_board, depth=remaining_depth)
            if move is None:
                break
            sequence.append(move)
            temp_board.push(move)
            if temp_board.is_checkmate():
                break
        return sequence


# ---------- Tkinter GUI ----------
CELL_SIZE = 60
BOARD_COLOR = ["#F0D9B5", "#B58863"]
CHESS_PIECES = {
    chess.PAWN: '♙', chess.KNIGHT: '♘', chess.BISHOP: '♗', chess.ROOK: '♖', chess.QUEEN: '♕', chess.KING: '♔',
    'black_pawn': '♟', 'black_knight': '♞', 'black_bishop': '♝', 'black_rook': '♜', 'black_queen': '♛', 'black_king': '♚'
}
symbol_to_name = {'p':'pawn','r':'rook','n':'knight','b':'bishop','q':'queen','k':'king'}

class ChessGUI:
    def __init__(self, root, solver, move_delay=1000):
        self.root = root
        self.solver = solver
        self.move_delay = move_delay
        self.canvas = tk.Canvas(root, width=8*CELL_SIZE, height=8*CELL_SIZE)
        self.canvas.pack()

        # Solve mate problem
        print("Solving mate problem...")
        self.sequence = solver.get_mate_sequence()
        print(f"Found sequence with {len(self.sequence)} moves: {[str(m) for m in self.sequence]}")

        self.move_index = 0
        self.draw_board()
        self.root.after(self.move_delay, self.animate_next_move)

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                color = BOARD_COLOR[(row + col) % 2]
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                # Map Tkinter row/col to chess square
                chess_row = 7 - row
                square = chess.square(col, chess_row)
                piece = self.solver.board.piece_at(square)
                if piece:
                    if piece.color == chess.WHITE:
                        text = CHESS_PIECES[piece.piece_type]
                    else:
                        name = symbol_to_name[piece.symbol().lower()]
                        text = CHESS_PIECES['black_' + name]
                    self.canvas.create_text(
                        x1 + CELL_SIZE // 2,
                        y1 + CELL_SIZE // 2,
                        text=text,
                        font=("Arial", 32)
                    )

    def animate_next_move(self):
        if self.move_index < len(self.sequence):
            move = self.sequence[self.move_index]
            print(f"Move {self.move_index + 1}: {move}")
            self.solver.board.push(move)
            self.draw_board()
            self.move_index += 1
            self.root.after(self.move_delay, self.animate_next_move)
        else:
            if self.solver.board.is_checkmate():
                print("Checkmate!")


# ---------- Run ----------
if __name__ == "__main__":
    # Example: Mate-in-3 puzzle
    fen = "r1b1qrk1/ppp2pp1/3p1PpQ/6B1/2B1PR2/2P4P/PP4P1/R5K1"
    solver = MateSolver(fen)

    # Set search depth explicitly: 4 plies for mate-in-2 set to 6 for mate in 3
    solver.set_search_depth(6)

    root = tk.Tk()
    root.title("Mate-in-N Solver GUI")
    gui = ChessGUI(root, solver, move_delay=1500)
    root.mainloop()
