import chess
import chess.engine

#ToDo: Check Same Pair of Moves for draw--
# Set up the board and engine
def PlayFullGame():
    board = chess.Board()
    engine= chess.engine.SimpleEngine.popen_uci(r"C:\Users\abhid\Downloads\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")

    # Play the game -- Lucas (Black) vs stockfish(White)
    while not board.is_game_over():
        
        if board.turn == chess.BLACK:
            #Put computer move from the system 
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
            
        
        # Try to make the move and update the board
    #     try:
    #         board.push(move)
    #     except chess.MoveError:
    #         print("Illegal move!")
    #         continue
        # Print the board
        board.push(move)
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