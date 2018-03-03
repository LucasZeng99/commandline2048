import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('2048GAME')

def log(msg):
    logger.info(msg)

class Game:
    def __init__(self):
        self.quit = False
        self.container = [[0 for x in range(4)] for i in range(4)]
        self.key = ''
        self.init_fill([3,4,5]) 

    def init_fill(self, arr):
        """arr: a list indicating the range of block # initially."""
        num_to_gen = random.choice(arr)
        for i in range(num_to_gen):
            self.container[random.choice(range(4))][random.choice(range(4))] = 2
            
    def score(self):
        a = []
        for row in range(4):
            a.append(sum(self.container[row]))
        return sum(a)
    def disp(self):
        new_matrix = self.container
        print("_____________________", flush=True)
        
        for r in range(4):
            
            print('|',end='')
            for c in range(4):
                if self.container[r][c] != 0:
                    print("{:4}".format(str(self.container[r][c])), end='', flush=True)
                else:
                    print("{:4}".format(" "), end='', flush=True)
                print('|', end='')
            print('', flush=True)
            print("—————————————————————", flush=True)
        print("score: {}".format(self.score()))

    def listenEvent(self):
        #return string input
        string = input('move:(w,a,s,d,q)')
        return string

    def getKeyDown(self, arr=''):
        """self.key = keydown. if is 'q' then self.quit = True"""
        while arr not in ['w', 'a', 's', 'd', 'q']:
            arr = input('try again:(w,a,s,d,q)')
        if arr == 'q':    
            self.quit = True
        self.key = arr

    def move(self, dir_vec):
        row_dir = dir_vec[0]
        col_dir = dir_vec[1]
        
        if col_dir != 0:
            for row in range(4):
                    # first delete all 0 then add to the right.
                while 0 in self.container[row]:
                    self.container[row].remove(0)
                while len(self.container[row]) < 4:
                    if col_dir == -1:
                        self.container[row].append(0)
                    elif col_dir == 1:
                        self.container[row] = [0] + self.container[row]
        else:
            new_matrix = []
            for col in range(4):
                # record every column in a mitrix of cols.
                one_col = []
                for row in range(4):
                    one_col.append(self.container[row][col])   
                # again, remove 0 first then add 0 in the tail or top.
                while 0 in one_col:
                    one_col.remove(0)
                while len(one_col) < 4:
                    if row_dir == -1:
                        one_col.append(0)
                    else:
                        one_col = [0] + one_col
                new_matrix.append(one_col)
            
            # replace the cols in container with new matrix.
            for col in range(4):
                for row in range(4):
                    self.container[row][col] = new_matrix[col][row]
    def add(self, dir_vec):
        row_dir = dir_vec[0]
        col_dir = dir_vec[1] 

        if col_dir != 0:
            for row in range(4):
                if col_dir == -1: #a
                    i = 0
                    while i < 3 and self.container[row][i] != self.container[row][i+1]:
                        i += 1
                    if i < 3:
                        this1 = self.container[row][i]
                        next1 = self.container[row][i+1]
                        if this1 == next1:
                            self.container[row][i] += next1
                            del(self.container[row][i+1])
                            self.container[row].append(0)
                if col_dir == 1: 
                    i = 3
                    while i > 0 and self.container[row][i] != self.container[row][i-1]:
                        i -= 1
                    if i > 0:
                        this1 = self.container[row][i]
                        next1 = self.container[row][i-1]
                        if this1 == next1:
                            self.container[row][i] += next1
                            del(self.container[row][i-1])
                            self.container[row] = [0] + self.container[row]
        else:# row_dir != 0
            new_matrix = []
            for col in range(4): 
                one_col = []
                for row in range(4):
                    one_col.append(self.container[row][col])
                new_matrix.append(one_col)
            if row_dir == 1: #s
                for col in range(4):
                    i = 3
                    while i > 0 and new_matrix[col][i] != new_matrix[col][i-1]:
                        i -= 1
                    if i > 0:
                        this = new_matrix[col][i]
                        next1 = new_matrix[col][i-1]
                        if this == next1:
                            new_matrix[col][i] += next1
                            del(new_matrix[col][i-1])
                            new_matrix[col] = [0] + new_matrix[col]                        
                
            elif row_dir == -1: # w
                for col in range(4):
                    i = 0
                    while  i < 3 and new_matrix[col][i] != new_matrix[col][i+1]:
                        i += 1

                    if i < 3:
                        this = new_matrix[col][i]
                        next1 = new_matrix[col][i+1]
                        if this == next1:
                            new_matrix[col][i] += next1
                            del(new_matrix[col][i+1])
                            new_matrix[col].append(0)
            
            for col in range(4):
                for row in range(4):
                    self.container[row][col] = new_matrix[col][row]
    def main(self, key):
        if key == 'w':
            self.move([-1, 0])
            self.add([-1, 0])
        elif key == 'a':
            self.move([0, -1])
            self.add([0, -1])
        elif key == 's':
            self.move([1, 0])
            self.add([1, 0])
        elif key == 'd':
            self.move([0, 1])
            self.add([0, 1])
        self.win()
    
    def generate(self, arr):
        points = []
        for row in range(4):
            for col in range(4):
                if self.container[row][col] == 0:
                    points.append([row, col])
        row_i, col_i = random.choice(points)
        self.container[row_i][col_i] = 2

    def win(self):
        for row in range(4):
            for col in range(4):
                if self.container[row][col] == 2048:
                    self.quit = True
game = Game()

while True and not game.quit:
    game.disp()
    game.getKeyDown(game.listenEvent()) # store key down to game.
    game.main(game.key)
    game.generate(1)
    