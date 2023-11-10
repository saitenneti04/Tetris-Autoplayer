from board import Direction, Rotation, Action
from random import Random
import time


class Player:
    def choose_action(self, board):
        raise NotImplementedError


class RandomPlayer(Player):
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
                

    def choose_action(self, board):
        self.print_board(board)
        time.sleep(0.5)
        if self.random.random() > 0.97:
            # 3% chance we'll discard or drop a bomb
            return self.random.choice([
                Action.Discard,
                Action.Bomb,
            ])
        else:
            # 97% chance we'll make a normal move
            return self.random.choice([
                Direction.Left,
                Direction.Right,
                Direction.Down,
                Rotation.Anticlockwise,
                Rotation.Clockwise,
            ])

class SaisPlayer(Player):
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
        sandbox = board.clone()
        if sandbox.next is None:
            return 0
        for i in range(rotation):
            sandbox.rotate(Rotation.Clockwise)

        if (min(x for (x,y) in sandbox.falling.cells) > a): 
            while (min(x for (x,y) in sandbox.falling.cells) > a):
                sandbox.move(Direction.Left)
        else:
            while (max(x for (x,y) in sandbox.falling.cells) < 9) and (min(x for (x,y) in sandbox.falling.cells) != a):
                sandbox.move(Direction.Right)       
        sandbox.move(Direction.Drop) 

        return self.scoreBoard(sandbox)
        
    def choose_action(self, board):
        #self.print_board(board)
        time.sleep(0.5)
        currentScore = 0
        xpos = 0
        rotation = 0
        for x in range(10):
            for rotations in range(4):
                if board.next != None:
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
        return min(y for (x,y) in sandbox.cells)
    




#SelectedPlayer = RandomPlayer
SelectedPlayer = SaisPlayer