#Import All Directories
import chess
import chess.engine
import CameraAndVision.TryPreProcessFinalSet as ProcessImage


# %run ".\ChessEngine\TrySimpleCall"
# TestCallFromAnotherFile()

PrevListOfTuples = []
PresentListOfTuples = []




#Human plays the move --> replies yes after playing on command-prompt
if __name__ == "__main__":
    # TryOCR()
    # board = chess.Board()
    # engine= chess.engine.SimpleEngine.popen_uci(r"C:\Users\abhid\Downloads\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")
    board = chess.Board()
    engine= chess.engine.SimpleEngine.popen_uci(r"C:\Users\abhid\Downloads\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")
    count = 0
    while not board.is_game_over():
        
        if board.turn == chess.WHITE:
            while True:
                # humanPlayed = input("Human Turn & press y ")    
                # move_str = "e2e4"  #From camera
                move_str = input("Human Turn & enter string ex- e2e4:")
                ProcessImage.CaptureImage(count)
                PresentListOfTuples = ProcessImage.ReturnTuple()


                print("Processing Human Played Movement--")
                print("Dividing into 64 blocks")
                print("Get FEN or displacement part")
                move = chess.Move.from_uci(move_str)
                # Check if the move is legal
                if move in board.legal_moves:
                    break
                else:
                    print("Illegal move! Try again.")
        else:
            #Robot Arm Turn
            print("Invoke Stockfish ")
            result = engine.play(board,chess.engine.Limit(time=2.0))
            move = result.move
            print("Output from engine is:")                
            print("Best move:", move)
            print("Robot Doing Motion")
            print("Robot Done")
            print("Take Image for played move ") 


                
        board.push(move)
        print(board)
        
        # Check if the game is over
        if board.is_game_over():
            result_str = str(board.result())
            
            if result_str == "1-0":
                print("White- Human wins!")
            elif result_str == "0-1":
                print("Black- RobotArm Lucas wins!")
            elif result_str == "1/2-1/2":
                print("Draw!")
            else:
                print("Unknown result:", result_str)
            break
                
    # Close the engine
    engine.close()        
             

#loop till game is over --
    #camera will take picture & process it to give difference 
    #Human movement -->ex: e2e4
    # ---> def CVForChess(img1 , img2): 
    #         return string e2e4

    #This movement ex-e2e4 is passed to chess engine --> 
    # chess engine predicts next move

    #Based on next move: say, g7g6 --> 
    #robot translates g7g6 to robotic path 
    # def RobotPlayMovement(string = "g7g6"):
    #     movemnt
    #     return str1 = done



    #camera takes image --> stores to use it for next movement processing 
    #prompt for human --> make next move
