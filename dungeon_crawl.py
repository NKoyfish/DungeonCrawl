"""
DungeonCrawl is a module that contains Cell, Maze, Enemy, Player, and an 
EmptyMaze type objects and some methods that generate Mazes or allows players
to battle against enemies. Mazes can also be parsed from a specifically
formatted file. Mazes begin with S and E and are bound by Walls. Mazes are made
up of cells with various obsID that represent different things you might
encounter in a dungeon. The goal of the player is to make it to the end of the
maze while collecting treasure and killing monsters along their path. Players
also run the risk of starving if they do not navigate through the dungeon quick
enough. Players have an inventory of tools that may aid them in their journey.

HOW TO RUN: python dungeon_crawl.py -filename maze3.txt
            or python dungeon_crawl.py
"""
from argparse import ArgumentParser
import sys
import curses
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
        isBorder: (Boolean) True if moving a Cell up left down or right isn't
                  a key
                    
    """
    def __init__(self,col,row,obsID):
        """
        Parameters:
                    col: (int) column number in Maze
                    row: (int) row number in Maze
                    obsID: (str) Cell type to be set
        Side effects: Initializes a new Cell object
        """
        self.col = col
        self.row = row
        self.pos = (row,col)
        self.obsID = obsID
        self.traveled = False
        self.playerthere = False
        self.revealed = False
        self.isBorder = False
        self.isInvisibleBorder = False

    def __repr__(self):
        """
        Allows Prints that reference a Cell object to print Cell.obsID
        Returns: Prints Cell.obsID, "?" if the Cell hasn't been revealed or "P" 
                 if the player is occupying the cell. 
        """
        if not self.playerthere and self.revealed:
            if self.obsID != "/":
                return (self.obsID)
            else: return " "
        if not self.revealed:
            if self.obsID != "/":
                return "?"
            else: return " "
        else:
            return "P"

class Player:
    """
    A Player explores a Maze. While exploring the maze their hunger goes down.
    Occasionally they may find an enemy that they must battle or run from.
    Players have skills they can use to traverse the maze easier.

    Attributes:
            name (str):         Represents the player
            health (float):     How much damage the player can take. Die at 0.
            maxHealth (float):  Cap of HP
            attack (float):     How much damage the player does.
            hunger (float):     How full the player is. 0 hunger is starving.
                                Starving players deal reduced damage and take 1
                                damage a turn
            battlesFought (int):How many battles the player has fought
            battlesWon (int):   How many battles the player has won
            treasureFound (int):How many T cells the player has passed over
            inventory (Dict):   A dictionary of strings representing items.
                                Values are ints representing the quantity owned
            abilityList (Dict): A dictionary of (str) skills the player can use 
                                and the remaining cooldown time until a skill 
                                can be used again. Every movement the player
                                makes reduces the cooldown (Value) by one. Rest
                                reduces the cooldown by 5.
    """                     
    def __init__(self,name,health,attack,hunger):
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
        Side effects: Initializes a new Player object
        """
        self.abilityList = {"break": 0, "jump": 0}
        self.name = name
        self.health = health
        self.maxhealth = health
        self.attack = attack
        self.hunger = hunger
        self.maxhunger = hunger
        self.speed = 70
        self.starve = False

class Enemy:
    """
    Nelson
    Brief Description: So there has been built an Enemy class that stores 3 
    methods that we will be using such as the __init__ method that will
    initialize the monsters_name, monsters_type, monsters_health, 
    speed and attack and the maxhealth of the enemy.
    We will be setting this in the near future allowing during creation
    These will be the attributes being used
    Attributes: 
    name (str) - this will be the monsters name
    type (str) - type of monster being battled
    health (int) - this will be the monsters health
    speed (int) - this will be the ability of the monsters speed
    attack (float) - this will be the monsters attack damage.
    """
    def __init__(self):
        """
        Explaination: 
            created a list called monsters which will hold all of the monsters 
            that we have allocated within the list and that we are going to use 
            within the maze.
            here we are referencing the monsters_name which will then
            grab a monster randomly using the randint function between 0-7 
            so anyone one of them from the list.
            - monsters_health is then set at 100 and based on the attack 
            and damage the health level will increase.
            - write a conditional that will determine attack or speed,
            depending on whether the randomizer chose 1 or 2 as the monster
            to fight the player. 

        """
        monsters = ["Zombie", "Kobold", "Orc", "Goblin",\
             "Skeleton", "Ghoul", "Lizardman", "Spectre"]
        self.name = monsters[randint(0,7)]
        montype = random.choice([1,1,1,1,1,1,1,2,2,2,3,3,3,4,4,5])
        
        if montype == 1:
            self.attack = randint(40,60)
            self.speed = randint(30,50)
            self.name = "Frail " + self.name
        elif montype == 2:
            self.attack = randint(50,65)
            self.speed = randint(40,55)
            self.name = "Haggard " + self.name
        elif montype == 3:
            self.attack = randint(60,75)
            self.speed = randint(50,70)
            self.name = "Skilled " + self.name
        elif montype == 4:
            self.attack = randint(75,95)
            self.speed = randint(55,60)
            self.name = "Elite " + self.name
        else:
            self.attack = randint(80,100)
            self.speed = randint(60,70)
            self.name = "Ancient " + self.name
        self.health = factorial(montype) * 5 + 100 

def strike(entity1,entity2):
    """TENTATIVE VERSION
    Entity1 attacks entity2 and calcualtes remaining hp

    Args:   entity1 (Player or Enemy)
            entity2 (Player or Enemy)
    
    Side effect: Lowers entity2 hp if an attack lands through them
    """
    baseAccuracy = .7
    critChance = 0
    critDmg = 1
    baseAccuracy += int((entity1.speed - entity2.speed)/4) / 100
    if entity1.speed - entity2.speed > 0:
        critChance = int((entity1.speed - entity2.speed)/5)
    
    if randint(0,100) < critChance:
        critDmg = 2.5
    if randint(0,100) <= baseAccuracy * 100:#accuracy roll
        entity2.health -= critDmg * randint[entity1.attack*.9,entity1.attack*1.1]
def battle_monsters(player, monster):
    """
    Args:
        player (Player) - this will be the player attacking the monster
        the monster.
        monster (Enemy) - this will be monster attacking the player
    Brief Description:
    here we are making a conditional that will determine who has won the battle.
    the first criteria would be if the player has no health and the monsters
    health is greater than the plyaer the monster has won the match. otherwise
    the monster has won. if the player and monsters health has reached a limit
    of 0, then that means that there has been a draw and nobody has won.
     maybe there could be a rematch.
    """
    battleEnd = False
    while not battleEnd:
        playerFaster = player.speed > monster.speed
        if playerFaster:
            strike(player,monster)
            if player.health == 0 and monster.health > player.health:
                print(f"{monster.name} has won the battle against\
                     {player.name}!")
            elif(monster.health == 0 and player.health > \
                monster.health):
                print(f"{player.name} won and {monster.name} \
                    has been defeated!")
            elif(player.health == 0 and monster.health == 0):
                print(f"{player.name} and {monster.name} \
                    have slain each other!") 
            strike(monster,player)
            if player.health == 0 and monster.health > player.health:
                print(f"{monster.name} has won the battle against \
                    {player.name}!")
            elif(monster.health == 0 and player.health \
                > monster.health):
                print(f"{player.name} won and {monster.name}\
                     has been defeated!")
            elif(player.health == 0 and monster.health == 0):
                print(f"{player.name} and {monster.name}\
                     have slain each other!")
            strike(monster,monster)
class EmptyMaze():
    """
    An EmptyMaze is created when generateSimpleMaze() is called.
    EmptyMaze starts off as an n by m sized rectangle designated by the user
    and procedurally generates start, end, treasure, and battle obstacles.

    Attributes:
        maxCol: (int) max number of columns in maze where index starts at 0.
        maxRow: (int) max number of rows in maze where index starts at 0.
        tuplemaze: (Dictionary of string casted tuples) keys pair with Cell objs
    """
    def __init__(self,mazefile):
        """
        Creates a new EmptyMaze object

        Parameters:
            mazefile: (str) name of new file to be made
        
        Side Effects:
            Creates a new EmptyMaze object
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

        Side effects: prints to stdout
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
    """
    A Maze has a Start and an End represented by S and E respectively
    The goal for a player in a maze is to get from S to E, battle enemies 
    and get treasure represented by B and T respectively. Reveals tiles
    the player has been near and may contain stairs that teleport the player.

    Attributes:
    tuplemaze (Dict):   a Dictionary of string keys
                        representing a string casted tuple of row,col.
                        Values are Cell Objects which contain tile data
                        needed to determine eligible tile traversal
    mazeStairs (Dict):  a Dictionary of single digit strings that have
                        a tuple containing two tuples. These two tuples
                        contain the location data of where a pair of stairs
                        lead to and switch when the player walks up the stairs
    modulePts (list):   A list of possible places to put a wall when generating
                        a maze if no txt file was given. A random point will be
                        selected and a wall in a random direction vertical 
                        or horizontal will be made along the point.
    currentTuple (tuple):a tuple containing the row and column of the curr loc
    current (str):       the string casted version of currentTuple used 
                            for easy dictionary retrieval
    endTuple (str):     The string of a tuple value in tuplemaze with obsID = E
    maxRow (int):       Total # of Cell rows in the maze used for iterating
    maxCol (int):       Total # of Cell columns in the maze used for iterating        
    """
    def __init__(self,mazefile,player):
        """
        Initializes a new Maze object

        Args:    mazefile (str):    path to the maze to be read from
                 player (Player):   Player currently running through the dungeon

        Side effects: Creates a new Maze object
        """
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
                        elif char == "/":
                            newCell = Cell(col,row,"/")
                            newCell.isInvisibleBorder = True
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
                self.modulePts = [self.modulePts[0],\
                    self.modulePts[len(self.modulePts)-1]]
        self.revealSurround()
        self.setBorders()
    def printMaze(self,player,bool = False):
        """
        prints the maze for the user to see current progress 
        and traversal options if bool is True then reveal the entire maze 
        (normally called after player death)

        Args: player (Player):  player participating in the maze
              bool (Boolean):   Reveal entire maze if True

        Side effects: prints to stdout
        """
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
            
    def breakWall(self,player):
        """
        breakWall allows a player to destroy a non bordering wall
        that are in proximity to the player (1 Cell away).

        Args:   
                direction (str) either "up", "down", "left", or "right"
                player (Player) the player breaking the wall.
        
        Side effects: Breaks a non bordering wall in front of the player.
        """
        row,col = self.currentTuple
        choose = False
        breakable = ["c"]
        dirs = { "up":"("+str(row-1)+", "+str(col)+")","down":"("+str(row+1)+\
        ", "+str(col)+")","left":"("+str(row)+", "+str(col-1)+")",\
                 "right":"("+str(row)+", "+str(col+1)+")"}
        if player.abilityList["break"] == 0:
            for wallCheck in dirs:
                if dirs[wallCheck] in self.tuplemaze.keys():
                    if self.tuplemaze[dirs[wallCheck]].obsID == "=" and \
                        not self.tuplemaze[dirs[wallCheck]].isBorder:
                        breakable.append(wallCheck)
            if len(breakable) > 1:
                while not choose:
                    print(breakable)
                    choice = input("What wall would you like to break or 'c' to cancel\n")
                    if choice == "c":
                        break
                    elif choice in breakable:
                        self.tuplemaze[dirs[choice]].obsID = " "
                        player.abilityList["break"] = 5
                        choose = True
            else: print("No wall to break")
        else: print("Break on cooldown for",player.abilityList["break"],"turns")
    def useTorch(self,player):
        """
        Torches are used by the player to reveal an extra tile of area around 
        the player. Torches can aid the player by increasing their accuracy on 
        monsters and can scare / debuff certain monsters. Torches will last a
        set amount ofsteps and will be tracked by a player attribute

        Args: player (Player): the player in the current dungeon run

        Side effects:   Removes a torch from the player's inventory, changes how
                        revealSurround() works, increases player accuracy
                        and may increase or decrease an Enemy class objects' dmg
        """
    pass #not yet implemented
    
    def getScore(self,player):
        """
        Calculates a score based off player attribute values, battles won, and
        treasure obtained.

        Returns: (Float) score value of the maze run after a run finishes via
                 player death or dungeon completion 
        """
        pass #not yet implemented

    def revealMap(self,player):
        """
        This reveals the game map if it is in the players inventory
        Args:
            player(Player): The name of the payer in the game
            search through the players inventory to find the map.
        Side effects: Makes the map entire layout visible and reveals treasure
        """
        print("Not yet implemented yet")

    def jumpWall(self, player):
        """
        this enables players who have the ability to jump over walls in the
        maze to be able to do so
        Args:
            player(String): The name of the player in the game
            it will evaluate the player and see if they have the ability to do
             so and if they can to execute, if not then the the code will break
        """
        pass #not implemented yet
    def move(self,player):
        """
        A players "turn" in a maze. Here they can decide to either move, rest,
        or perform a skill.

        Args:
                player: (Player) the player about to perform an action.
        Side effects:   Prints to stdout and changes attributes such as
                        player health and hunger. Maze revealed via
                        revealSurround()
        """
        resp = input("\nMove where? (u)p,(d)own,(l)eft, or (r)ight\n \
        Other: (Rest), (B)reak Wall or (P)osition\n")
        moved = False
        tupUp = self.currentTuple #THIS IS NOT A STRING YET
        row,col = tupUp
        if resp in ["u","up"]:
            up = str(self.currentTuple)
            tupNewUp = "("+str(row-1)+", "+str(col)+")"
            if tupNewUp in self.tuplemaze.keys() and \
                self.tuplemaze[tupNewUp].obsID != "=":

                self.tuplemaze[up].playerthere = False
                self.currentTuple = (row-1,col)
                self.tuplemaze[tupNewUp].playerthere = True
                moved = True
            else: print("A wall obstructs you")
        elif resp in ["d","down"]:
            up = str(self.currentTuple)
            tupNewUp = "("+str(row+1)+", "+str(col)+")"

            if tupNewUp in self.tuplemaze.keys() and \
                self.tuplemaze[tupNewUp].obsID != "=":

                self.tuplemaze[up].playerthere = False
                self.currentTuple = (row+1,col)
                self.tuplemaze[tupNewUp].playerthere = True
                moved = True
            else: print("A wall obstructs you")
        elif resp in ["l","left"]:
            up = str(self.currentTuple)
            tupNewUp = "("+str(row)+", "+str(col-1)+")"
            if tupNewUp in self.tuplemaze.keys() and\
                self.tuplemaze[tupNewUp].obsID != "=":

                self.tuplemaze[up].playerthere = False
                self.currentTuple = (row,col-1)
                self.tuplemaze[tupNewUp].playerthere = True
                moved = True
            else: print("A wall obstructs you")
        elif resp in ["right","r"]:
            up = str(self.currentTuple)
            tupNewUp = "("+str(row)+", "+str(col+1)+")"
            if tupNewUp in self.tuplemaze.keys() and\
                self.tuplemaze[tupNewUp].obsID != "=":

                self.tuplemaze[up].playerthere = False
                self.currentTuple = (row,col+1)
                self.tuplemaze[tupNewUp].playerthere = True
                moved = True
            else: print("A wall obstructs you")
        if self.tuplemaze[str(self.currentTuple)].obsID.isdigit():#stair check
            print("move from", self.currentTuple)
            print(self.tuplemaze[str(self.currentTuple)].playerthere)
            self.revealSurround() #Have to reveal surrounding area before
            # moving somewhere new
            pos1,pos2 = self.mazeStairs\
                [self.tuplemaze[str(self.currentTuple)].obsID]
            self.tuplemaze[str(self.currentTuple)].playerthere = False
            if self.currentTuple == pos1:
                self.currentTuple = pos2
            else:
                self.currentTuple = pos1
            self.tuplemaze[str(self.currentTuple)].playerthere = True
            self.tuplemaze[str(self.currentTuple)].revealed = True
        if moved: #reduce hunger or health and cooldowns
            for ability in player.abilityList.keys():
                if player.abilityList[ability] > 0:
                    player.abilityList[ability] -= 1
            if player.hunger > 0:
                player.hunger -= 1
            else: player.health -=1

            if player.health == 0: #death check
                print(f"{player.name} has died of starvation")
        elif resp.lower() == "b": #breakWall
            self.breakWall(player)
        elif resp == "p": # used primarily for debugging
            print(self.currentTuple)

        elif resp.lower() == "rest":
            if player.hunger > 10:
                player.health += player.maxhealth/10
                if player.health > player.maxhealth:
                    player.health = player.maxhealth
                player.hunger -= 10
                for ability in player.abilityList.keys():
                    if player.abilityList[ability] > 0:
                        player.abilityList[ability] -= 5
                    if player.abilityList[ability] < 0:
                        player.abilityList[ability] = 0
        else: print("invalid direction or action")
        self.revealSurround()
    def setBorders(self):
        #print([self.tuplemaze[cell].obsID for cell in self.tuplemaze.keys()])
        for cell in self.tuplemaze.keys():
            cellKey = cell
            cell = cell.replace("(","")
            cell = cell.replace(")","")
            row = int(cell.split(", ") [0])
            col =  int(cell.split(", ") [1])
            #print(row,col)
            dirs = { "up":"("+str(row-1)+", "+str(col)+")",\
                "down":"("+str(row+1)+", "+str(col)+")",\
                "left":"("+str(row)+", "+str(col-1)+")",\
                "right":"("+str(row)+", "+str(col+1)+")"}

            for dire in dirs.keys():
                if dirs[dire] not in self.tuplemaze.keys() or self.tuplemaze[dirs[dire]].obsID == "/":
                    self.tuplemaze[cellKey].isBorder = True
    def getBorder(self):
        borderList = []
        for cell in self.tuplemaze.keys():
            if self.tuplemaze[cell].isBorder:
                borderList.append(cell)
        return borderList

    def revealSurround(self):
        """
        Reveals the surrounding maze area (one cell away from the player 
        and two if the player has a torch)

        Side effect: changes self.revealed to True if player in proximity.
        """
        row,col = self.currentTuple
        dirs ={ "up":"("+str(row-1)+", "+str(col)+")",\
                "down":"("+str(row+1)+", "+str(col)+")",
                "left":"("+str(row)+", "+str(col-1)+")", \
                "right":"("+str(row)+", "+str(col+1)+")",\
                "upl":"("+str(row-1)+", "+str(col-1)+")",
                "downl":"("+str(row+1)+", "+str(col-1)+")",\
                "upR":"("+str(row-1)+", "+str(col+1)+")",\
                "downR":"("+str(row+1)+", "+str(col+1)+")"}
        #currently only reveals one tile, 2 to be added soon        
        for key in dirs.keys():
            if dirs[key] in self.tuplemaze.keys():
                self.tuplemaze[dirs[key]].revealed = True
        
def generateSimpleMaze():
    """
    Creates a simple maze if the user didnt provide a txt file to be read from.

    Side effect: Creates a new maze and prints to stdout. Creates a txt file of
                 the maze that writes to the local path named temp.txt before
                 getting deleted but used for a new file named generated.txt
                 that completes the maze creation
    Returns: filename of newly created maze txt file to be read from
    """
    with open("temp.txt", "w+") as f: 
        wall = "="
        space = " "  
        roomConditionMet = False
        
        while not roomConditionMet:
            rowsize = int(input("How many rows? (Enter value >= 6)\n"))
            colsize = int(input("How many columns? (Enter value >= 6)\n"))
            mazeArea = (rowsize-2)*(colsize-2)
            if colsize >= 6 and rowsize >= 6:
                roomConditionMet = True
            else:
                print("Impossible to do, enter a smaller number")

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
    #These 3 lists ensure that non Start and End tiles aren't overlapped by B or T
    #After all you can't start / end a maze if S / E got overidden by T or B.
    occupied = ["."]
    illegalrow = [0]
    illegalcol = [0]
    anchorrow = 0
    anchorcol = 0
    while startloc == endloc:#Make unique start and end points
        srow,scol = (random.randint(1,newMaze.maxRow-1),\
            random.randint(1,newMaze.maxCol-1))
        erow,ecol = (random.randint(1,newMaze.maxRow-1),\
            random.randint(1,newMaze.maxCol-1))
        if "("+ str(srow) + "," + str(scol) + ")" \
        != "("+ str(erow) + "," + str(ecol) + ")":
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
    #Both get set to True once an appropriate col and row are found
    while anchorrow in illegalrow and anchorcol in illegalcol:
        if not ancR:
            anchorrow = random.randint(2,newMaze.maxRow-2)  
        if not ancC:
            anchorcol = random.randint(2,newMaze.maxCol-2)
        if anchorrow not in illegalrow:
            ancR = True
        if anchorcol not in illegalcol:
            ancC = True
    #print((anchorrow,anchorcol))
    r = 0
    c = 0
    #make a wall vertical or horizontal from the anchor point
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
    #populate the maze rectangle in proportion to its size with B and T
    #also ensures that they dont overlap with start and end points or other B Ts
    for count in range(int(area/20)+1):
        while battleloc in occupied and treasureloc in occupied:
            battleloc = "("+ str(random.randint(1,newMaze.maxRow-1))+", "\
                + str(random.randint(1,newMaze.maxCol-1))+")"
            treasureloc = "("+ str(random.randint(1,newMaze.maxRow-1))+", "\
                + str(random.randint(1,newMaze.maxCol-1))+")"
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
    """
    Sets the stage for playing and the difficulty. Lower levels of hunger
    makes the game much harder.

    Args:
            maze (str):     txt file name to read maze from.
            hunger (float): max hunger for the player
    
    Side effects:
                    prints to stdout and makes a new maze
                    lowers player hunger as turns progress
                    reveals maze tiles as player progresses
    """
    if maze is None:
        maze = generateSimpleMaze()
    player = Player("Nick",10,3,hunger)
    newMaze= Maze(maze,player)
    #print(f"Max c: {newMaze.maxCol}, Max r: {newMaze.maxRow}")
    newMaze.printMaze(player)
    #borders = set(newMaze.getBorder())
    #cells = set(newMaze.tuplemaze.keys())
    #diff = cells - borders
    #print(diff)
    while str(newMaze.currentTuple) != str(newMaze.endTuple) and player.health > 0:
        newMaze.move(player)
        newMaze.printMaze(player)
        newMaze.getBorder()
    if player.health == 0:
        print("\nGame Over!")
        newMaze.printMaze(player,True)
    else: print("\nCompleted Maze!")

def parse_args(arglist):
    """ Parse command-line arguments.
    
    Expect two mandatory arguments:
        - filename: name of the file
        -
    Optional Args to be ad:
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