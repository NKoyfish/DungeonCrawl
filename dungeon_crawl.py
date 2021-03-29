from argparse import ArgumentParser
import sys


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
    def smile():
        print("hello") 
        print("hi")
    def __init__(self,col,row,obsID):
        """
        Parameters:
                    col: (int) column number in Maze
                    row: (int) row number in Maze
                    obsID: (str) Cell type to be set
        
        """
        self.col = col
        self.row = row
        self.obsID = obsID
        self.traveled = False
        self.playerthere = False
        self.revealed = False

    def __repr__(self):
        """
        Prints Cell.obsID
        Side Effect: Prints Cell obsID or P if player occupies the Cell.
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
class Maze:
    def __init__(self,mazefile,player):
        self.mazeDict = {}
        self.current = "c0,0"
        row = -1
        col = 0
        with open(mazefile,"r") as f:
            for line in f.readlines():
                col = 0
                row +=1
                for char in line:
                    cell = "c" + str(row) +","+ str(col) 
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
                self.revealSurround()
    def wherePlayer(self):
        """
        returns the position of the player.
        """
        for key in self.mazeDict.keys():
            if self.mazeDict[key].playerthere:
                temp = self.mazeDict[key]
                return "c"+ str(temp.row) +","+ str(temp.col)
    
    def printMaze(self,player):
        statsShown = False
        for r in range(self.maxRow+1):
            if r >0:
                print()
            for c in range(self.maxCol+1):
                name = "c" + str(r) + ","+ str(c)
                if name in self.mazeDict.keys():
                    if self.mazeDict[name].playerthere:
                        print("P",end ="")
                    else:
                        print(self.mazeDict[name],end ="")
        if not statsShown:
            print(f"\nHealth: {player.health}/{player.maxhealth} \t \
                Hunger: {player.hunger}/{player.maxhunger}")
            statsShown = True
    def move(self,player):
        resp = input("\nMove where? (u)p,(d)own,(l)eft, or (r)ight\n \
        Other: (Rest), or (p)osition\n")
        moved = False
        if resp in ["u","up"]:
            up = self.current
            newUp = "c"+str(int((up.split(",")[0])[1:])-1)+ ","+up.split(",")[1]
            if newUp in self.mazeDict.keys() and self.mazeDict[newUp].obsID != "=":
                self.mazeDict[up].playerthere = False
                self.current = newUp
                self.mazeDict[newUp].playerthere = True
                moved = True
            else: print("A wall obstructs you")
        elif resp in ["d","down"]:
            up = self.current
            newUp = "c"+str(int((up.split(",")[0])[1:])+1)+ ","+up.split(",")[1]
            #print(newUp)
            if newUp in self.mazeDict.keys() and self.mazeDict[newUp].obsID != "=":
                self.mazeDict[up].playerthere = False
                self.current = newUp
                self.mazeDict[newUp].playerthere = True
                moved = True
            else: print("A wall obstructs you")
        elif resp in ["l","left"]:
            up = self.current
            newUp = up.split(",")[0] + ","+ str(int((up.split(",")[1]))-1) 
            #print(newUp)
            if newUp in self.mazeDict.keys() and self.mazeDict[newUp].obsID != "=":
                self.mazeDict[up].playerthere = False
                self.current = newUp
                self.mazeDict[newUp].playerthere = True
                moved = True
            else: print("A wall obstructs you")
        elif resp in ["right","r"]:
            up = self.current
            newUp = up.split(",")[0] + ","+ str(int((up.split(",")[1]))+1) 
            #print(newUp)
            if newUp in self.mazeDict.keys() and self.mazeDict[newUp].obsID != "=":
                self.mazeDict[up].playerthere = False
                self.current = newUp
                self.mazeDict[newUp].playerthere = True 
                moved = True
            else: print("A wall obstructs you")
        if moved:
            if player.hunger > 0:
                player.hunger -= 1
            else: player.health -=1

            if player.health == 0:
                print(f"{player.name} has died of starvation")

        elif resp == "p":
            print(self.wherePlayer())

        elif resp.lower() == "rest":
            if player.hunger > 10:
                player.health += player.maxhealth/10
                if player.health > player.maxhealth:
                    player.health = player.maxhealth
                player.hunger -= 10
        
        else: print("invalid direction or action")
        #print("new: ",self.current)
        self.revealSurround()
        self.printMaze(player)
    def revealSurround(self):
        curr = self.current
        surround = ["c"+str(int((curr.split(",")[0])[1:])-1)+ ","+curr.split(",")[1], 
        "c"+str(int((curr.split(",")[0])[1:])-1) + ","+ str(int((curr.split(",")[1]))+1), 
        "c"+str(int((curr.split(",")[0])[1:])-1) + ","+ str(int((curr.split(",")[1]))-1),
        "c"+str(int((curr.split(",")[0])[1:])+1)+ ","+curr.split(",")[1], 
        "c"+str(int((curr.split(",")[0])[1:])+1) + ","+ str(int((curr.split(",")[1]))+1), 
        "c"+str(int((curr.split(",")[0])[1:])+1) + ","+ str(int((curr.split(",")[1]))-1),
        curr.split(",")[0] + ","+ str(int((curr.split(",")[1]))-1),
        curr.split(",")[0] + ","+ str(int((curr.split(",")[1]))+1)]
        for closeCell in surround:
            if closeCell in self.mazeDict.keys():
                self.mazeDict[closeCell].revealed = True
def main(maze,hunger = 50):
    player = Player("Nick",10,3,hunger)
    newMaze= Maze(maze,player)
    #print(f"Max c: {newMaze.maxCol}, Max r: {newMaze.maxRow}")
    newMaze.printMaze(player)
    while newMaze.current != newMaze.end and player.health > 0:
        newMaze.move(player)
    if player.health == 0:
        print("\nGame Over!")
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
    parser.add_argument("filename",
                        help="path to maze layout")
    return parser.parse_args(arglist)
if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.filename)    