from board import Direction, Rotation, Action
from random import Random
import time
global_counter = 0


class Player:
    def choose_action(self, board):
        raise NotImplementedError



class Version5(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)

    def moveTowardTarget(self, a, rotation, board):
        landed = False
        sandbox = board.clone()

        for i in range(rotation):
            landed = sandbox.rotate(Rotation.Clockwise)
            if landed:
                break

        if (min(x for (x,y) in sandbox.falling.cells) > a): 
            while (min(x for (x,y) in sandbox.falling.cells) > a):
                landed = sandbox.move(Direction.Left)
                if landed:
                    break

        else:
            while (max(x for (x,y) in sandbox.falling.cells) < 9) and (min(x for (x,y) in sandbox.falling.cells) != a):
                landed = sandbox.move(Direction.Right)
                if landed: 
                    break
     
        if not landed:
            sandbox.move(Direction.Drop) 


        return self.scoreBoard(sandbox)
        
    def choose_action(self, board):
        #self.print_board(board)
        currentScore = -100000000
        xpos = 0
        rotation = 0
        for x in range(10):
            for rotations in range(4):

                score = self.moveTowardTarget(x, rotations, board)
                if score > currentScore:
                    currentScore = score
                    xpos = x
                    rotation = rotations
       
 
        for i in range(rotation):
            yield Rotation.Clockwise

        if (min(x for (x,y) in board.falling.cells) > xpos): 
            while (min(x for (x,y) in board.falling.cells) > xpos):
                yield Direction.Left
        else:
            while (max(x for (x,y) in board.falling.cells) < 9) and (min(x for (x,y) in board.falling.cells) != xpos):
                yield Direction.Right     

        yield Direction.Drop     

    
    def scoreBoard(self, sandbox):
        score = 0
        score += self.uniformHeights(sandbox)
        score += self.boardGaps(sandbox)
        score += self.minHeight(sandbox)
        return score
    
    #max height
    def minHeight(self, sandbox):
        return 1 * min(y for (x,y) in sandbox.cells)
    
    #bumps
    def uniformHeights(self, sandbox):
        
        score = 0

        lowest_y_for_x = {x: 23 for x in range(10)}

        for (x,y) in sandbox.cells:
            if y < lowest_y_for_x[x]:
                lowest_y_for_x[x] = y

        for i in range(9):
            score += abs(lowest_y_for_x[i] - lowest_y_for_x[i+1])
        
        return -1.3 * (score)

    

    def boardGaps(self, sandbox):
        score = 0
        for x in range(sandbox.width):
            for y in range(sandbox.height): 
                if (x,y) in sandbox.cells:
                    for a in range(y+1, sandbox.height):
                        if (x, a) not in sandbox.cells:
                            score -=11.4
                    break

        return score
    
    


  
#SelectedPlayer = Version1
#SelectedPlayer = Version2
SelectedPlayer = Version5