from argparse import ArgumentParser
import sys

class Cell:
    def __init__(self,col,row,obsID):
        self.col = col
        self.row = row
        self.obsID = obsID
        self.traveled = False
        self.playerthere = False
    def __repr__(self):
        if not self.playerthere:
            return (self.obsID)
        else:
            return "P"
class Player:
    def __init__(self,name,weapondmg,hunger,location):
        self.name = name
        self.weapon = weapondmg
        self.hunger = hunger
        row,col = location
        self.location = row,col
class Maze:
    def __repr__(self):
        print("hi")
    def wherePlayer(self):
        for key in self.mazeDict.keys():
            if self.mazeDict[key].playerthere:
                return self.mazeDict[key]
    def printMaze(self):
        for r in range(self.maxRow+1):
            if r > 0:
                print()
            for c in range(self.maxCol+1):
                name = "c" + str(r) + str(c)
                if name in self.mazeDict.keys():
                    if self.mazeDict[name].playerthere:
                        print("P",end ="")
                    else:
                        print(self.mazeDict[name],end="")
    def move(self):
        resp = input("\nMove where? up,down,left, or right\n")
        if resp == "up":
            up = self.current
            newUp = "c" + str(int(up[1]) - 1) + up[2]
            if newUp in self.mazeDict.keys() and self.mazeDict[newUp].obsID != "=":
                self.mazeDict[up].playerthere = False
                self.current = newUp
                self.mazeDict[newUp].playerthere = True
            else: print("invalid move")
        elif resp == "down":
            up = self.current
            newUp = "c" + str(int(up[1]) + 1) + up[2]
            if newUp in self.mazeDict.keys() and self.mazeDict[newUp].obsID != "=":
                self.mazeDict[up].playerthere = False
                self.current = newUp
                self.mazeDict[newUp].playerthere = True
            else: print("invalid move")
        elif resp == "left":
            up = self.current
            newUp = "c" + up[1] + str(int(up[2]) - 1)
            if newUp in self.mazeDict.keys() and self.mazeDict[newUp].obsID != "=":
                self.mazeDict[up].playerthere = False
                self.current = newUp
                self.mazeDict[newUp].playerthere = True
            else: print("invalid move")
        elif resp == "right":
            up = self.current
            newUp = "c" + up[1] + str(int(up[2]) + 1)
            if newUp in self.mazeDict.keys() and self.mazeDict[newUp].obsID != "=":
                self.mazeDict[up].playerthere = False
                self.current = newUp
                self.mazeDict[newUp].playerthere = True
            else: print("invalid move")
        else: print("invalid direction")
        self.printMaze()

    def __init__(self,mazefile,player):
        self.mazeDict = {}
        row = -1
        col = 0
        with open(mazefile,"r") as f:
            for line in f.readlines():
                col = 0
                row +=1
                for char in line:
                    cell = "c" + str(row) + str(col) 
                    if char == "=":
                        newCell = Cell(col,row,"=")
                        self.mazeDict[cell] = newCell
                    elif char == "S":
                        newCell = Cell(col,row,"S")
                        newCell.playerthere = True
                        self.mazeDict[cell] = newCell
                        self.current = cell          
                    elif char == "E":
                        newCell = Cell(col,row,"E")
                        self.mazeDict[cell] = newCell
                        self.end = cell
                    else:
                        newCell = Cell(col,row," ")
                        self.mazeDict[cell] = newCell
                    col+=1
                self.maxCol = col -1
                self.maxRow = row

def main(maze,hunger = 50):
    x = 0
    player = Player("Nick",3,hunger,(0,0))
    newMaze= Maze(maze,player)
    player.location = (1,0)
    print(f"Max c: {newMaze.maxCol}, Max r: {newMaze.maxRow}")
    #while player.location != (newMaze.end[1],newMaze.end[2]):
    newMaze.printMaze()
    while newMaze.current != newMaze.end:
        newMaze.move()
def parse_args(arglist):
    """ Parse command-line arguments.
    
    Expect two mandatory arguments:
        - 
        -
        
    Args:
        arglist (list of str): arguments from the command line.
    
    Returns:
        namespace: the parsed arguments, as a namespace.
    """
    parser = ArgumentParser()
    parser.add_argument("filename",
                        help="path to maze layout")
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.filename)    