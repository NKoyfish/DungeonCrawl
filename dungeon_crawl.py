from argparse import ArgumentParser
import sys
import tempfile
import os
import random

class Cell:
    """
    A Cell makes up a Maze Object. The most basic Cells are walls and open
    spaces.

    Attributes:
        col: (int) What column the Cell is located (index starts at 0)
        row: (int) What row the Cell is located in (index starts at 0)
        obsID: (str) What the Cell is acting as:
                    "=": Represents a Wall and is impassible* 
                    "S": Where the Maze starts
                    "E": Where the Maze ends
                    " ": An open spot to travel to
                    "T": Treasure (Adds to score) can contain equipment,torches
                         or food
                    "B": Initiates a battle encounter. See Maze.battle()
                    "#": Stairs to the next floor. Pairs with another floor with
                         the same number
        traveled: (Boolean) True if a player has traveled there or false if not
        playerthere: (Boolean) Represents if player is currently occupying Cell
        revealed: (Boolean) True if the player has traveled near the Cell
                    
    """
    def __init__(self,col,row,obsID):
        """
        Parameters:
                    col: (int) column number in Maze
                    row: (int) row number in Maze
                    obsID: (str) Cell type to be set
        
        """
        self.col = col
        self.row = row
        self.pos = (row,col)
        self.obsID = obsID
        self.traveled = False
        self.playerthere = False
        self.revealed = False

    def __repr__(self):
        """
        Allows Prints that reference a Cell object to print Cell.obsID
        Returns: Prints Cell.obsID, "?" if the Cell hasn't been revealed or "P" if the
                 player is occupying the cell. 
        """
        if not self.playerthere and self.revealed:
            return (self.obsID)
        if not self.revealed:
            return "?"
        else:
            return "P"

class Player:
    """
    A Player explores a Maze. While exploring the maze their hunger goes down.
    Occasionally they may find an enemy that they must battle or run from.
    Players have skills they can use to traverse the maze easier.

    Attributes:
                name (str): Represents the player
                health (float): How much damage the player can take. Die at 0.
                maxHealth (float): Cap of HP
                weapondmg (float): How much damage the player does.
                hunger (float): How full the player is. 0 hunger is starving.
                                Starving players deal reduced damage and take 1
                                damage a turn
    """
    def __init__(self,name,health,weapondmg,hunger):
        """
        Initializes a new Player object

        Parameters:
                    name (str): name of the new player
                    health (float): HP of the new player
                    maxHealth (float): maxHP of the new player
                    weapondmg (float): Attack damage of the player
                    hunger (float): How full the player is
                    maxHunger (float): Max hunger of the player
                    starve (boolean): Is the player at 0 hunger?
        """
        self.name = name
        self.health = health
        self.maxhealth = health
        self.weapon = weapondmg
        self.hunger = hunger
        self.maxhunger = hunger
        self.starve = False

class EmptyMaze():
    def __init__(self,mazefile):
        self.tuplemaze = {}
        row = -1
        col = 0
        with open(mazefile,"r") as f:
            for line in f.readlines():
                col = 0
                row +=1
                for char in line.strip(): #get rid of newlines
                    strTuple = str((row,col))
                    if char == "=":
                        newCell = Cell(col,row,"=")
                        self.tuplemaze[strTuple] = newCell
                    
                    else:
                        newCell = Cell(col,row," ")
                        self.tuplemaze[strTuple] = newCell
                    col+=1
                self.maxCol = col -1
                self.maxRow = row

    def printMaze(self):
        for r in range(self.maxRow+1):
            if r >0:
                print()
            for c in range(self.maxCol+1):
                name = "("+str(r)+", "+str(c)+")"
                if name in self.tuplemaze.keys():
                    self.tuplemaze[name].revealed = True
                    print(self.tuplemaze[name],end ="")
class Maze():
    def __init__(self,mazefile,player):
        self.mazeDict = {}
        self.mazeStairs = {}
        self.tuplemaze = {}
        self.currentTuple = "not set"
        self.current = "not set"
        self.endTuple = "not set"
        row = -1
        col = 0
        with open(mazefile,"r") as f:
            for line in f.readlines():
                col = 0
                row +=1
                for char in line.strip(): #get rid of newlines
                    strTuple = str((row,col))
                    if char == "=":
                        newCell = Cell(col,row,"=")
                        self.tuplemaze[strTuple] = newCell
                    elif char == "S":
                        newCell = Cell(col,row,"S")
                        newCell.playerthere = True
                        self.tuplemaze[strTuple] = newCell
                        self.currentTuple = (row,col)          
                    elif char == "E":
                        newCell = Cell(col,row,"E")
                        self.tuplemaze[strTuple] = newCell
                        self.endTuple = strTuple
                    elif char == "T":
                        newCell = Cell(col,row,"T")
                        self.tuplemaze[strTuple] = newCell
                    elif char == "B":
                        newCell = Cell(col,row,"B")
                        self.tuplemaze[strTuple] = newCell
                    elif char.isdigit(): #stairs
                        newCell = Cell(col,row,char)
                        newCell.obsID = char
                        self.tuplemaze[strTuple] = newCell
                        if char not in self.mazeStairs.keys():
                            self.mazeStairs[char] = ((row,col),"")
                            #first detection of a stair number 
                        else:
                            pos1,pos2 = self.mazeStairs[char]
                            pos2 = (row,col)
                            self.mazeStairs[char] = (pos1,pos2)
                    else:
                        newCell = Cell(col,row," ")
                        self.tuplemaze[strTuple] = newCell
                    col+=1
                self.maxCol = col -1
                self.maxRow = row
        self.revealSurround()
    
    def printMaze(self,player,bool = False):
        statsShown = False
        for r in range(self.maxRow+1):
            if r >0:
                print()
            for c in range(self.maxCol+1):
                name = "("+str(r)+", "+str(c)+")"
                if name in self.tuplemaze.keys():
                    if self.tuplemaze[name].playerthere:
                        print("P",end ="")
                    else:
                        if not bool:
                            print(self.tuplemaze[name],end ="")
                        else: print(self.tuplemaze[name].obsID,end ="")
        if not statsShown:
            print(f"\nHealth: {player.health}/{player.maxhealth} \t \
                Hunger: {player.hunger}/{player.maxhunger}")
            statsShown = True
    
    def move(self,player):
        resp = input("\nMove where? (u)p,(d)own,(l)eft, or (r)ight\n \
        Other: (Rest), or (p)osition\n")
        moved = False
        tupUp = self.currentTuple #THIS IS NOT A STRING YET
        row,col = tupUp
        if resp in ["u","up"]:
            up = str(self.currentTuple)
            tupNewUp = "("+str(row-1)+", "+str(col)+")"
            if tupNewUp in self.tuplemaze.keys() and self.tuplemaze[tupNewUp].obsID != "=":
                self.tuplemaze[up].playerthere = False
                self.currentTuple = (row-1,col)
                self.tuplemaze[tupNewUp].playerthere = True
                moved = True
            else: print("A wall obstructs you")
        elif resp in ["d","down"]:
            up = str(self.currentTuple)
            tupNewUp = "("+str(row+1)+", "+str(col)+")"
            if tupNewUp in self.tuplemaze.keys() and self.tuplemaze[tupNewUp].obsID != "=":
                self.tuplemaze[up].playerthere = False
                self.currentTuple = (row+1,col)
                self.tuplemaze[tupNewUp].playerthere = True
                moved = True
            else: print("A wall obstructs you")
        elif resp in ["l","left"]:
            up = str(self.currentTuple)
            tupNewUp = "("+str(row)+", "+str(col-1)+")"
            if tupNewUp in self.tuplemaze.keys() and self.tuplemaze[tupNewUp].obsID != "=":
                self.tuplemaze[up].playerthere = False
                self.currentTuple = (row,col-1)
                self.tuplemaze[tupNewUp].playerthere = True
                moved = True
            else: print("A wall obstructs you")
        elif resp in ["right","r"]:
            up = str(self.currentTuple)
            tupNewUp = "("+str(row)+", "+str(col+1)+")"
            if tupNewUp in self.tuplemaze.keys() and self.tuplemaze[tupNewUp].obsID != "=":
                self.tuplemaze[up].playerthere = False
                self.currentTuple = (row,col+1)
                self.tuplemaze[tupNewUp].playerthere = True
                moved = True
            else: print("A wall obstructs you")
        if self.tuplemaze[str(self.currentTuple)].obsID.isdigit():#stair check
            print("move from", self.currentTuple)
            print(self.tuplemaze[str(self.currentTuple)].playerthere)
            pos1,pos2 = self.mazeStairs[self.tuplemaze[str(self.currentTuple)].obsID]
            self.tuplemaze[str(self.currentTuple)].playerthere = False
            if self.currentTuple == pos1:
                self.currentTuple = pos2
            else:
                self.currentTuple = pos1
            self.tuplemaze[str(self.currentTuple)].playerthere = True
            self.tuplemaze[str(self.currentTuple)].revealed = True
        if moved:
            if player.hunger > 0:
                player.hunger -= 1
            else: player.health -=1

            if player.health == 0:
                print(f"{player.name} has died of starvation")

        elif resp == "p":
            print(self.currentTuple)

        elif resp.lower() == "rest":
            if player.hunger > 10:
                player.health += player.maxhealth/10
                if player.health > player.maxhealth:
                    player.health = player.maxhealth
                player.hunger -= 10
        
        else: print("invalid direction or action")
        self.revealSurround()
    
    def revealSurround(self):
        row,col = self.currentTuple
        dirs ={ "up":"("+str(row-1)+", "+str(col)+")","down":"("+str(row+1)+", "+str(col)+")",
                "left":"("+str(row)+", "+str(col-1)+")", "right":"("+str(row)+", "+str(col+1)+")",
                "upl":"("+str(row-1)+", "+str(col-1)+")","downl":"("+str(row+1)+", "+str(col-1)+")",
                "upR":"("+str(row-1)+", "+str(col+1)+")", "downR":"("+str(row+1)+", "+str(col+1)+")"}
        for key in dirs.keys():
            if dirs[key] in self.tuplemaze.keys():
                self.tuplemaze[dirs[key]].revealed = True

def generateSimpleMaze():
        with open("temp.txt", "w+") as f: 
            wall = "="
            space = " "  
            rowsize = int(input("How many rows? (Enter value > 3)\n"))
            colsize = int(input("How many columns? (Enter value > 3)\n"))
            #rooms = int(input("How many rooms?\n"))
            for x in range(rowsize):
                if x == 0 or x== rowsize-1:
                    wallstr = wall*colsize+"\n"
                    #print(wallstr,end="")
                    f.write(wallstr)
                else:
                    wallstr = "="+ space*(colsize-2)+"=\n"
                    f.write(wallstr)
                    #print(wallstr,end="")
        newMaze = EmptyMaze("temp.txt")
        startloc = "."
        endloc = "."
        occupied = ["."]
        while startloc == endloc:
            startloc = "("+ str(random.randint(1,newMaze.maxRow-1))+", "+ str(random.randint(1,newMaze.maxCol-1))+")"
            endloc = "("+ str(random.randint(1,newMaze.maxRow-1))+", "+ str(random.randint(1,newMaze.maxCol-1))+")"
        newMaze.tuplemaze[startloc].obsID="S"
        newMaze.tuplemaze[endloc].obsID="E"
        occupied.append(startloc)
        occupied.append(endloc)
        area = (newMaze.maxCol - 2) * (newMaze.maxRow-2)
        battleloc = "."
        treasureloc = "."
        
        for count in range(int(area/20)+1):
            while battleloc in occupied and treasureloc in occupied:
                battleloc = "("+ str(random.randint(1,newMaze.maxRow-1))+", "+ str(random.randint(1,newMaze.maxCol-1))+")"
                treasureloc = "("+ str(random.randint(1,newMaze.maxRow-1))+", "+ str(random.randint(1,newMaze.maxCol-1))+")"
            if battleloc not in occupied:
                newMaze.tuplemaze[battleloc].obsID ="B"
                occupied.append(battleloc)
            if treasureloc not in occupied:
                newMaze.tuplemaze[treasureloc].obsID ="T"
                occupied.append(treasureloc)
        with open("generated.txt","w") as g:
            for cell in newMaze.tuplemaze.keys():
                if newMaze.tuplemaze[cell].col == newMaze.maxCol:
                    g.write("=")
                    g.write("\n")
                else:
                    g.write(newMaze.tuplemaze[cell].obsID)
        
        os.remove("temp.txt")
        return g.name

def main(maze,hunger = 50):
    if maze is None:
        maze = generateSimpleMaze()
    player = Player("Nick",10,3,hunger)
    newMaze= Maze(maze,player)
    #print(f"Max c: {newMaze.maxCol}, Max r: {newMaze.maxRow}")
    newMaze.printMaze(player)
    while str(newMaze.currentTuple) != str(newMaze.endTuple) and player.health > 0:
        newMaze.move(player)
        newMaze.printMaze(player)
    if player.health == 0:
        print("\nGame Over!")
        newMaze.printMaze(player,True)
    else: print("\nCompleted Maze!")

def parse_args(arglist):
    """ Parse command-line arguments.
    
    Expect two mandatory arguments:
        - filename: name of the file
        -
    Optional Args:
        - mobs: allows for roaming mobs to spawn 
        - torch: reveals surrounding cells in a bigger area.

    Args:
        arglist (list of str): arguments from the command line.
    
    Returns:
        namespace: the parsed arguments, as a namespace.
    """
    parser = ArgumentParser()
    parser.add_argument("-filename",
                        help="path to maze layout")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.filename)    