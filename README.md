# RobotPlayingChess1

-- Robotic Arm Playing Chess Against Human
-- Steps:
  1) Human Plays the Move
  2) Camera Takes Image -- 
      a)Processes to Give all 64 blocks 
      b) checks for right move or not
          i) if right move , continue
          ii) if wrong move -- give another turn to play
      
  3) Stockfish + Python Chess to predict next move
  4) This predicted move is given to Robotic Arm which is then performed & says done
  5) Camera takes image -- 
      a)Processes to Give all 64 blocks 
      b) checks for right move or not
          i) if right move , continue
          ii) if wrong move -- give another turn to play
  6) Repeat steps 1 to 5 while game is over 
