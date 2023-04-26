#Import All Directories
import chess
import chess.engine
# import CameraAndVision.TryPreProcessFinalSet as ProcessImage
import CameraAndVision.vision_api as Vision

# %run ".\ChessEngine\TrySimpleCall"
# TestCallFromAnotherFile()

ListOfPieces = ['p', 'q', 'r', 'n', 'b','k','P', 'Q','R','N', 'B','K']


def GetUciMove(listOfTuples1, listOfTuples2):
    result_uci = ""
    countOfPiecesMoved = 0
    listOfPiecesMoved = []
    #loop through each item
    for i  in range(len(listOfTuples1)):
        #if firstloc is full & secondloc is empty --> this piece moved -- prev_uci 
        #if firstloc is empty & secondloc is full --> this piece destinatio -- next_uci
        locationInFirstBoard = listOfTuples1[i][1]
        locationIn2ndBoard = listOfTuples2[i][1]

        if (locationInFirstBoard in ListOfPieces) and locationIn2ndBoard == "*":
            listOfPiecesMoved.append(locationInFirstBoard)
            countOfPiecesMoved = countOfPiecesMoved + 1
            prev_uci = listOfTuples1[i][0]
        elif locationInFirstBoard == "*" and (locationIn2ndBoard in ListOfPieces):
            next_uci = listOfTuples1[i][0]
        else:
            continue

    if countOfPiecesMoved > 1:
        print("From Past Move to Present Move --multiple moves detected")
        print(listOfPiecesMoved)
    else:
        result_uci = prev_uci + next_uci

    return result_uci

listOfTuples = [('a1', 'R'), ('a2', 'P'), ('a3', '*'), ('a4', '*'), ('a5', '*'), ('a6', '*'), ('a7', 'p'), ('a8', 'r'), ('b1', 'N'), ('b2', 'P'), ('b3', '*'), ('b4', '*'), ('b5', '*'), ('b6', '*'), ('b7', 'p'), ('b8', 'n'), ('c1', 'B'), ('c2', 'P'), ('c3', '*'), ('c4', '*'), ('c5', '*'), ('c6', '*'), ('c7', 'p'), ('c8', 'b'), ('d1', 'K'), ('d2', 'P'), ('d3', '*'), ('d4', '*'), ('d5', '*'), ('d6', '*'), ('d7', 'p'), ('d8', 'k'), ('e1', 'Q'), ('e2', 'P'), ('e3', '*'), ('e4', '*'), ('e5', '*'), ('e6', '*'), ('e7', 'p'), ('e8', 'q'), ('f1', 'B'), ('f2', 'P'), ('f3', '*'), ('f4', '*'), ('f5', '*'), ('f6', '*'), ('f7', 'p'), ('f8', 'b'), ('g1', 'N'), ('g2', 'P'), ('g3', '*'), ('g4', '*'), ('g5', '*'), ('g6', '*'), ('g7', 'p'), ('g8', 'n'), ('h1', 'R'), ('h2', 'P'), ('h3', '*'), ('h4', '*'), ('h5', '*'), ('h6', '*'), ('h7', 'p'), ('h8', 'r')]

PrevListOfTuples = []
PresentListOfTuples = listOfTuples
PathForCHessEngine = r"C:\Users\soura\Downloads\stockfish_15.1_win_x64_avx2\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe"
#Human plays the move --> replies yes after playing on command-prompt
if __name__ == "__main__":
    # TryOCR()
    # board = chess.Board()
    # engine= chess.engine.SimpleEngine.popen_uci(r"C:\Users\abhid\Downloads\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")
    board = chess.Board()
    # engine= chess.engine.SimpleEngine.popen_uci(r"C:\Users\abhid\Downloads\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")

    engine= chess.engine.SimpleEngine.popen_uci(PathForCHessEngine)
    count = 0
    while not board.is_game_over():
        
        if board.turn == chess.WHITE:
            while True:
                humanPlayed = input("After Human moves, Press any key to coninue: ")    
                # move_str = "e2e4"  #From camera
                # move_str = input("Human Turn & enter string ex- e2e4:")
                # ProcessImage.CaptureImage(count)
                PrevListOfTuples = PresentListOfTuples
                PresentListOfTuples = Vision.PreProcessImage(count)
                move_str = GetUciMove(PrevListOfTuples , PresentListOfTuples)
                print("Move by CV = {}".format(move_str))
                # print("Processing Human Played Movement--")
                # print("Dividing into 64 blocks")
                # print("Get FEN or displacement part")
                move = chess.Move.from_uci(move_str)
                # Check if the move is legal
                if move in board.legal_moves:
                    count = count + 1
                    break
                else:
                    print("Illegal move! Try again.")
        else:
            #Robot Arm Turn
            print("Invoke Stockfish ")
            result = engine.play(board,chess.engine.Limit(time=2.0))
            move = result.move
            print(board)
            print("move by Chess Engine:{}".format(move))
            robot_played = input("After Robot has moved, press any key to continue:")

            PrevListOfTuples = PresentListOfTuples
            PresentListOfTuples = Vision.PreProcessImage(count)
            move_str1 = GetUciMove(PrevListOfTuples , PresentListOfTuples)
            print("move by Chess Engine:{}".format(move))
            print("move by vision:{}".format(move_str1))
            #To Do : Add code for illegal moves 
            #check for engine & arm --same 
            count = count + 1
            # print("Robot Doing Motion")
            # print("Robot Done")
            # print("Take Image for played move ") 
            

                
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
