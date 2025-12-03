import tkinter as tk
import chess
import math


class MateSolver:
    def __init__(self, fen_string=None):
        self.MATE_SCORE = 100000
        self.STALEMATE_SCORE = 0
        self.board = chess.Board(fen_string) if fen_string else chess.Board()
        self.start_board = self.board.copy()
        self.search_depth = 4  #default depth in plies
        self.nodes_searched = 0 #tracking nodes
        self.MAX_NODES = 200_000 #node limit for gui


    def set_search_depth(self, depth):
        self.search_depth = depth

    def evaluate_position(self, board, depth):
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                return -self.MATE_SCORE + depth  #black mated NEGATIVE SCORE
            else:
                return self.MATE_SCORE - depth   #white mated HIGH POSITIVE SCORE
        if board.is_stalemate():
            return 0

        #piece material scoring
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
    
    def ordered_moves(self, board):
        moves = list(board.legal_moves)

        def score_move(move):
            score = 0

            #checks this first
            board.push(move)
            if board.is_check():
                score += 10000
            board.pop()

            #check if capture
            if board.is_capture(move):
                score += 5000

            return score

        moves.sort(key=score_move, reverse=True)
        return moves


    def minimax_alpha_beta_search(self, board, depth=None, alpha=-math.inf, beta=math.inf):
        if depth is None:
            depth = self.search_depth

        #stop search if we exceed max nodes
        self.nodes_searched += 1
        if self.nodes_searched > self.MAX_NODES:
            return self.evaluate_position(board, depth), None
        
        #base case if depth is 0 or game is over
        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board, depth), None

        maximizing = board.turn == chess.WHITE
        best_move = None

        if maximizing:
            #white wants to maximize
            max_eval = -math.inf

            #iterate over ordered moves
            for move in self.ordered_moves(board):
                board.push(move) #do the move
                eval_score, _ = self.minimax_alpha_beta_search(board, depth - 1, alpha, beta)
                board.pop() #undo the move

                #update the best score and move
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                    # early mate cutoff
                    if max_eval >= self.MATE_SCORE - depth:
                        return max_eval, best_move
                    
                #alpha update and pruning check
                alpha = max(alpha, max_eval)
                if beta <= alpha: #beta cutoff
                    break
            return max_eval, best_move
        else:
            #black wants to minimize
            min_eval = math.inf

            for move in self.ordered_moves(board):
                board.push(move) #do the move
                eval_score, _ = self.minimax_alpha_beta_search(board, depth - 1, alpha, beta)
                board.pop() #undo the move
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                    # early mate cutoff 
                    if min_eval <= -self.MATE_SCORE + depth:
                        return min_eval, best_move
                    
                #alpha update and pruning check
                beta = min(beta, min_eval)
                if beta <= alpha: #beta cutoff
                    break
            return min_eval, best_move

    def get_mate_sequence(self):
        #return sequence of nodes towards mate
        sequence = []
        temp_board = self.board.copy()

        #reset counter before searching
        self.nodes_searched = 0

        for move_num in range(self.search_depth):

            #remaining depths shrinks as we step
            remaining_depth = self.search_depth - move_num

            #use minimax to find best move
            score, move = self.minimax_alpha_beta_search(temp_board, depth=remaining_depth)

            #if no legal moves available then stop
            if move is None:
                break
            sequence.append(move)
            temp_board.push(move)
            if temp_board.is_checkmate():
                break
        return sequence


#gui
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

        #get the mate sequence
        self.sequence = []
        self.move_index = 0
        self.draw_board()

         #buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        #solve button
        self.solve_button = tk.Button(button_frame, text="Solve", command=self.solve)
        self.solve_button.pack(side=tk.LEFT, padx=5)

        #next step button
        self.step_button = tk.Button(button_frame, text="Next Move", command=self.step)
        self.step_button.pack(side=tk.LEFT, padx=5)

    def solve(self):
        print("Solving mate problem...")
        self.solver.board = self.solver.start_board.copy()
        self.sequence = self.solver.get_mate_sequence()
        self.move_index = 0
        print(f"Found sequence: {[str(m) for m in self.sequence]}")

    def step(self):
        if self.move_index < len(self.sequence):
            move = self.sequence[self.move_index]
            print(f"Move {self.move_index + 1}: {move}")
            self.solver.board.push(move)
            self.draw_board()
            self.move_index += 1



    def draw_board(self):
        self.canvas.delete("all")

        #generate the 8x8 board
        for row in range(8):
            for col in range(8):
                color = BOARD_COLOR[(row + col) % 2]
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                #Map Tkinter row/col to chess square
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


if __name__ == "__main__":
    #insert fen codes
    fen = "2B5/8/3K4/1p6/2k5/P4P2/1B6/N4N2 w - - 0 1"
    solver = MateSolver(fen)

    #adjust depth, set to 4 for mate in 2, set to 6 for mate in 3
    solver.set_search_depth(4)

    root = tk.Tk()
    root.title("Mate-in-N Solver GUI")
    gui = ChessGUI(root, solver, move_delay=1500)
    root.mainloop()
