from argparse import ArgumentParser
import sys
import tempfile
import os
import math
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
    
    #might need to alter later but this is where i'm thinking about
    #putting the battle method. 
    """
      Brief Description: this battle method will be created, the player 
      will be faced with a creature or a person to fight and 
      the user will choose if he wants to run away from the battle, fight 
      the battle or rest, allow the player to recuperate, eat something
      and some back to battle.

      this for now is a brainstorming idea!
    """
    #Temporarily we are using the pass functionality to 
    #act as a place holder for our battle_enemy method since we dont
    #have a proper method yet.
    def buildEnemy(self):
        monsters = ["Aaragorn", "Legolas", "Gimli", "Gandalf", "Golum", "Dufus", "Rico", "Joker"]
        self.monsters_name = monsters[randint(0,7)]
        self.monsters_type = randint(1,2)
        self.monsters_health = 100

        if self.monsters_type == 1:
            self.monsters_strength = randint(70,90)
            self.monsters_speed = randint(50,70)
        elif self.monsters_type == 2:
            self.monsters_strength = randint(50,70)
            self.monsters_speed = randint(70,90)

    #getting the information
    def getEnemy(self):
        self.monsterSTATS = [self.monsters_name, self.monsters_type, self.monsters_strength, self.monsters_speed, self.monsters_health]
        return self.monsterSTATS

    #so far this is what i have!
    def battle_monsters(player, monster):
        if player.maxhealth == 0 and monster.maxhealth > player.maxhealth:
            print(f"{monster.monsters_name} has won the battle against {player.name}!")
        elif(monster.maxhealth == 0 and player.maxhealth > monster.maxhealth):
            print(f"{player.name} won and {monster.monsters_name} has been defeated!")
        elif(player.maxhealth == 0 and monster.maxhealth == 0):
            print()
            print(f"{player.name} and {monster.monsters_name} has made amends!") 
    

class EmptyMaze():
    """
    An EmptyMaze is created when generateSimpleMaze() is called.
    EmptyMaze starts off as an n by m sized rectangle designated by the user
    and procedurally generates start, end, treasure, and battle obstacles.

    Attributes:
        maxCol: (int) max number of columns in maze where index starts at 0.
        maxRow: (int) max number of rows in maze where index starts at 0.
        tuplemaze: (Dictionary of string casted tuples) keys pair with Cell objects
    """
    def __init__(self,mazefile):
        """
        Creates a new EmptyMaze object

        Parameters:
            mazefile: (str) name of new file to be made
        
        Side Effects:
            sets self.maxCol
            sets self.maxRow
        """
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
        """
        prints the EmptyMaze
        only really used for debugging dungeon generation
        """
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
        self.modulePts = [] #attachment pts for generateSimpleMaze()
        self.currentTuple = "not set"
        self.current = "not set"
        self.endTuple = "not set"
        row = -1
        col = 0
        with open(mazefile,"r") as f:
            for line in f.readlines():
                col = 0
                row +=1
                for char in line: #get rid of newlines
                    if char != "\n":
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
                    else: 
                        self.modulePts.append((row,col-1))
                self.maxCol = col -1
                self.maxRow = row
                self.modulePts = [self.modulePts[0],self.modulePts[len(self.modulePts)-1]]
        self.revealSurround()
    
    def printMaze(self,player,bool = False):
        statsShown = False
        print(self.modulePts)
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

    def writeMaze(self,file):
        """
        Converts a Maze object back into a textfile. Used to append new rooms

        Parameters:
                file: (str) name to the file to be created temporarily

        Side Effects:
                creates a new txt file in the current directory named file
        """
        with open(file,"w") as f:
            maxrowcount = 0
            r = 0
            print("max",self.maxRow)
            while maxrowcount < self.maxRow+1:
                for c in range(self.maxCol+1):
                    strTup = "("+str(maxrowcount)+", "+str(c)+")"
                    strTupplus = "("+str(maxrowcount)+", "+str(c+1)+")"
                    if strTupplus in self.tuplemaze.keys():
                        f.write(self.tuplemaze[strTup].obsID)
                    else:
                        f.write(self.tuplemaze[strTup].obsID)
                        if c != self.maxCol+1:
                            f.write("\n")
                maxrowcount +=1
            

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

    def appendRoom(self,maze2,open = True):
        print("d")
        
def generateSimpleMaze(newRoom = False):
        with open("temp.txt", "w+") as f: 
            wall = "="
            space = " "  
            roomConditionMet = False
            rowsize = int(input("How many rows? (Enter value > 3)\n"))
            colsize = int(input("How many columns? (Enter value > 3)\n"))
            rooms = 0
            mazeArea = (rowsize-2)*(colsize-2)
            if colsize > 5 and rowsize > 5:
                while not roomConditionMet:
                    rooms = int(input("How many rooms?")) 
                    if math.floor(mazeArea/9) < rooms:
                        print("Impossible to do, enter a smaller number")
                    else: roomConditionMet = True

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
        illegalrow = [0]
        illegalcol = [0]
        anchorrow = 0
        anchorcol = 0
        while startloc == endloc:
            srow,scol = (random.randint(1,newMaze.maxRow-1),random.randint(1,newMaze.maxCol-1))
            erow,ecol = (random.randint(1,newMaze.maxRow-1),random.randint(1,newMaze.maxCol-1))
            if (str(srow),str(scol)) != (str(erow),str(ecol)):
                startloc = "("+ str(srow)+", "+ str(scol)+")"
                endloc = "("+ str(erow)+", "+ str(ecol)+")"
                newMaze.tuplemaze[startloc].obsID="S"
                newMaze.tuplemaze[endloc].obsID="E"
                occupied.append(startloc)
                occupied.append(endloc)
                illegalcol.append(ecol)
                illegalcol.append(scol)
                illegalrow.append(erow)
                illegalrow.append(srow)
        ancR = False
        ancC = False
        while anchorrow in illegalrow and anchorcol in illegalcol:
            if not ancR:
                anchorrow = random.randint(2,newMaze.maxRow-2)  
            if not ancC:
                anchorcol = random.randint(2,newMaze.maxCol-2)
            if anchorrow not in illegalrow:
                ancR = True
            if anchorcol not in illegalcol:
                ancC = True
        print((anchorrow,anchorcol))
        r = 0
        c = 0
        if random.choice(["vert","horiz"]) == "vert":
            while r < newMaze.maxRow+1:
                roll = random.uniform(0, 1)
                if roll < .8:
                    strTup = "(" + str(r) +", " + str(anchorcol) + ")"
                    if strTup in newMaze.tuplemaze.keys():
                        newMaze.tuplemaze[strTup].obsID = "="
                r+=1
        else:
            while c < newMaze.maxCol+1:
                roll = random.uniform(0, 1)
                if roll < .8:
                    strTup = "(" + str(anchorrow) +", " + str(c) + ")"
                    if strTup in newMaze.tuplemaze.keys() and \
                        newMaze.tuplemaze[strTup].obsID not in ["S","E"]:
                        newMaze.tuplemaze[strTup].obsID = "="
                c+=1

        
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