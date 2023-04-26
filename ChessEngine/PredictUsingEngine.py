import chess
import chess.engine

PathEngine = r"C:\\Users\\abhid\Downloads\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe"
#ToDo: Check Same Pair of Moves for draw--
# Set up the board and engine
def PlayFullGame():
    board = chess.Board()
    engine= chess.engine.SimpleEngine.popen_uci(r"C:\Users\abhid\Downloads\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")

    fen = board.fen()
    print("init board fen")
    print(fen)
    # Play the game -- Lucas (Black) vs stockfish(White)
    countOfHalfMoves = 0
    countOfFullMoves = 1
    while not board.is_game_over():
        
        if board.turn == chess.BLACK:
            #Put computer move from the system 
            countOfHalfMoves = countOfHalfMoves + 1
            countOfFullMoves = countOfFullMoves + 1
            while True:
                
                move_str = input("Enter computer move:")
                move = chess.Move.from_uci(move_str)
                # Check if the move is legal
                if move in board.legal_moves:
                    break
                else:
                    print("Illegal move! Try again.")
                
        else:
            #Put Ur move using stockfish engine
            result = engine.play(board,chess.engine.Limit(time=2.0))
            move = result.move
            print("Best move:", move)
            countOfHalfMoves = countOfHalfMoves + 1
            
        
        # Try to make the move and update the board
    #     try:
    #         board.push(move)
    #     except chess.MoveError:
    #         print("Illegal move!")
    #         continue
        # Print the board
        board.push(move)
        fen = board.fen()
        print(fen)
        # print("countOfHalfMoves = {}".format(countOfHalfMoves))
        print("countOfFullMoves = {}".format(countOfFullMoves))

        print(board)
        # Check if the game is over
        if board.is_game_over():
            result_str = str(board.result())
            
            if result_str == "1-0":
                print("White- You(Stockfish) wins!")
            elif result_str == "0-1":
                print("Black-(Computer) Lucas wins!")
            elif result_str == "1/2-1/2":
                print("Draw!")
            else:
                print("Unknown result:", result_str)
            break
                
    # Close the engine
    engine.close()

class ChessEngine:
    def __init__(self) -> None:
        board = chess.Board()
        engine = chess.engine.SimpleEngine.popen_uci(PathEngine)

    
def InitBoardAndEngine():
    board = chess.Board()
    engine= chess.engine.SimpleEngine.popen_uci(r"C:\Users\abhid\Downloads\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")


def GetMoveFrom2Fens(prev_fen , present_fen):

    # Define the two FEN strings
    # fen_str1 = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    # fen_str2 = 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'

    fen_str1 = prev_fen
    fen_str2 = present_fen

    # Create Board objects from the FEN strings
    board1 = chess.Board(fen_str1)
    board2 = chess.Board(fen_str2)

    # Determine the move that was made
    move = None
    for possible_move in board2.legal_moves:
        if board1.copy().push(possible_move) == board2:
            move = possible_move
            break

    # Convert the move to UCI notation
    uci_string = move.uci()

    # Print the UCI move string
    print(uci_string)

    #Another code
    # Get the move needed to get from board1 to board2
    move = board2.uci().replace(board1.uci(), '')



if __name__ == "__main__":
    PlayFullGame()