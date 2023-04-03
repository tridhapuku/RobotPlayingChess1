#Import All Directories


def TryImportLibtest():
    import matplotlib.pyplot as plt
    x = [1,2,3]
    y = [1,2,3]

    plt.plot(x,y)
    plt.show()
    return

def TestCallFromAnotherFile():
    # %run ".\ChessEngine\TrySimpleCall"
    import ChessEngine.PredictUsingEngine as PredictByEngine 

    # PredictByEngine.
    # import sys
    # sys.path.append('D:\\MS_Related\\ASU\\CSE598_Robotics\RobotPlayingChess\ChessEngine')
    # import TrySimpleCall
    # Func()
    # return
#Just Begin

def TestCallFromSameFolder():
    import File1
    File1.welcomeall()
    return

print("Hello World")
TestCallFromSameFolder()
# %run ".\ChessEngine\TrySimpleCall"
# TestCallFromAnotherFile()


#Human plays the move --> replies yes after playing on command-prompt


#camera will take picture & process it to give difference 
#Human movement -->ex: e2e4

#This movement ex-e2e4 is passed to chess engine --> 
# chess engine predicts next move

#Based on next move: say, g7g6 --> 
#robot translates g7g6 to robotic path 

#camera takes image --> stores to use it for next movement processing 
#prompt for human --> make next move