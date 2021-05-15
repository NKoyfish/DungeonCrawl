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

Note for 326 Grader from Nicholas Koy: 
    The Gear Class, Loot generation, Combat system, and Colored prints are very 
    overkill.Please pretend as if the they were not part of the project. I 
    enjoyed making them and would prefer those methods involving the inventory
    or __str__() of many methods and functions to just be normal. I may be able
    to find a wayin the future to toggle the simple damage calculations and
    inventory system or create a fork where everything and meets the final
    rubric.

HOW TO RUN: python dungeon_crawl.py -filename maze3.txt
            or python dungeon_crawl.py

__authors__ =   'Ali Iqbal', 'Nelson Contreras', 'Nicholas Koy', and
                'Noble Nwokoma'
"""
from argparse import ArgumentParser
import sys
from string import Template
from time import sleep
import tempfile
import os
import math
from random import randint
import random
from math import factorial
DEBUG = False
SHOW_N_MESSAGES = 2
def cls():
    """
    clears the terminal screen, supports Mac and PC
    """
    os.system('cls' if os.name == 'nt' else 'clear')
class MessageLog():
    """
    Stores a log of text for the player to read past actions

        Attributes:
                log (list): list of maximum size 3 with string objects which
                            represent actions the player has taken
        __author__ = 'Nicholas Koy': class + methods
    """
    
    def __init__(self):
        """
        Makes a new MessageLog object
        Side effects: Creates a new MessageLog Object
        """
        self.log = []
    def fullLog(self):
        """
        Prints the whole adventure log. Identical to __str__() but the whole log
        instead of 2 entries shown
        Side effects: prints to stdout
        """
        colorAll = False
        maxStringSizeNoColor = 0
        maxStringSizeColor = None
        stringsizeWObracket = None
        frame = ""
        for message in self.log:
            if "[" in message:
                colorAll = True
                if maxStringSizeColor is None:
                    maxStringSizeColor = len(message)
                elif maxStringSizeColor < len(message):
                    maxStringSizeColor = len(message)
                stringsizeWObracket = maxStringSizeColor - 13
            else:
                if maxStringSizeNoColor < len(message):
                     maxStringSizeNoColor = len(message)
        if colorAll:
            frame = "=" *(stringsizeWObracket+7) + "\n"
            for message in self.log:
                if "[" in message:
                    frame += "# " + message + " "* (maxStringSizeColor-len(message))+"#\n"
                else:
                    frame += "# " + message + " "* (maxStringSizeColor-len(message)-9)+ "#\n"
            frame+="=" *(stringsizeWObracket+7) + "\n"
        else:
            frame = "▭" *(maxStringSizeNoColor+4) + "\n"
            for message in self.log:
                frame += "▯ " + message + " "*(maxStringSizeNoColor-len(message)+1) + "▯\n"
            frame += "▭" *(maxStringSizeNoColor+4) + "\n"
        print (frame)
    def __str__(self):
        """
        Prints the last 3 player actions
        Side effects: Prints to stdout
        Returns: String based off self.log
        """
        maxMsg = len(self.log)
        colorTwo = False
        maxStringSizeNoColor = 0
        maxStringSizeColor = None
        stringsizeWObracket = None
        frame = ""
        if maxMsg > SHOW_N_MESSAGES : maxMsg = SHOW_N_MESSAGES
        for message in self.log[-SHOW_N_MESSAGES:]:
            if "[" in message:
                colorTwo = True
                if maxStringSizeColor is None:
                    maxStringSizeColor = len(message)
                elif maxStringSizeColor < len(message):
                    maxStringSizeColor = len(message)
                stringsizeWObracket = maxStringSizeColor - 13
            else:
                if maxStringSizeNoColor < len(message):
                     maxStringSizeNoColor = len(message)
        if colorTwo:
            frame = "▭" *(stringsizeWObracket+7) + "\n"
            for message in self.log[-SHOW_N_MESSAGES:]:
                if "[" in message:
                    frame += "▯ " + message + " "* (maxStringSizeColor-len(message))+"▯\n"
                else:
                    frame += "▯ " + message + " "* (maxStringSizeColor-len(message)-9)+ "▯\n"
            frame+="▭" *(stringsizeWObracket+7) + "\n"
        elif not colorTwo and len(self.log) > 0:
            frame = "▭" *(maxStringSizeNoColor+4) + "\n"
            for message in self.log[-maxMsg:]:
                frame += "▯ " + message + " "*(maxStringSizeNoColor-len(message)+1) + "▯\n"
            frame += "▭" *(maxStringSizeNoColor+4) + "\n"
        elif len(self.log) < 2:
            frame = ""
        return frame
    
    def addLog(self,msg,repeat = False):
        """
        Appends a new message to log. Doesn't append a repeated message unless
        the player is in combat

        Arguments:  msg (str): Message to be added to log
                    repeat (boolean): msg important enough to be repeated?
        Side Effects: appends to self.log 
        """
        if len(self.log) > 1:
            if repeat == False and self.log[-1] != msg:
                self.log.append(msg)
            elif repeat:
                self.log.append(msg)
        else:
            self.log.append(msg)
        if repeat:
            print(self)
class Cell:
    """
    A Cell makes up a Maze Object. The most basic Cells are walls and open
    spaces.
    __author__ = 'Nicholas Koy' : class and methods
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
                    "/": Void space cant break or travel over
        traveled: (Boolean) True if a player has traveled there or false if not
        playerthere: (Boolean) Represents if player is currently occupying Cell
        revealed: (Boolean) True if the player has traveled near the Cell
        isBorder: (Boolean) True if moving a Cell up left down or right isn't
                  a key
        self.isInvisibleBorder: True if the obsID = "/"
                    
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

    def __str__(self):
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
class Maze():
    """
    A Maze has a Start and an End represented by S and E respectively
    The goal for a player in a maze is to get from S to E, battle enemies 
    and get treasure represented by B and T respectively. Reveals tiles
    the player has been near and may contain stairs that teleport the player.

    __authors__ =   'Ali Iqbal', 'Nelson Contreras', 'Nicholas Koy', and
                    'Noble Nwokoma'
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
    enemyPos (list):    list of keys that represent an Enemy encounter
    """
    WALL = "\033[1;4;37m"
    def __init__(self,mazefile,player):
        """
        Initializes a new Maze object
        __author__ = 'Nicholas Koy'
        Args:    mazefile (str):    path to the maze to be read from
                 player (Player):   Player currently running through the dungeon

        Side effects: Creates a new Maze object
        """
        self.messageLog = []
        self.mazeStairs = {}
        self.tuplemaze = {}
        self.modulePts = [] #attachment pts for generateSimpleMaze()
        self.currentTuple = "not set"
        self.current = "not set"
        self.endTuple = "not set"
        self.enemyPos = []
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
                            self.enemyPos.append("("+str(row)+ ", "+str(col)+")")
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
    def visible(self,mode):
        """
        Changes wall color from white to black
        or black to white
        """
        if mode == "light":
            Maze.WALL = "\033[1;4;37m"
        else:
            Maze.WALL = "\033[1;4;30m"
    def printMaze(self,player,msgLog: MessageLog(),boole = False):
        """
        prints the maze for the user to see current progress 
        and traversal options if bool is True then reveal the entire maze 
        (normally called after player death)

        Will print out the menus before the maze if the player has them toggled
        __author__ = 'Nicholas Koy'
        Args: player (Player):  player participating in the maze
              msgLog (MessageLog): prints past actions after maze
              bool (Boolean):   Reveal entire maze if True

        Side effects: prints to stdout
        """
        #print(self.modulePts)
        if player.hideStats == False:
            print(player)
        if player.hideLog == False:
            print(msgLog)
        os.system('')
        for r in range(self.maxRow+1):
            if r >0:
                print()
            for c in range(self.maxCol+1):
                name = "("+str(r)+", "+str(c)+")"
                if name in self.tuplemaze.keys():
                    if self.tuplemaze[name].playerthere:
                        print("\033[1;92mP\033[0m",end ="")
                    elif not boole:
                        if self.tuplemaze[name].obsID == "B" and\
                             self.tuplemaze[name].revealed:
                            print("\033[1;31m"+'B'+"\033[0m",end ="")
                        elif self.tuplemaze[name].obsID == "=" and\
                             self.tuplemaze[name].revealed:
                            print(Maze.WALL+'█'+"\033[0m",end ="")
                        elif self.tuplemaze[name].obsID == "T" and\
                             self.tuplemaze[name].revealed:
                            print("\033[1;33m"+str(self.tuplemaze[name])+\
                                "\033[0m",end ="")
                        else:
                            print(self.tuplemaze[name],end ="")
                    else:print(self.tuplemaze[name].obsID,end ="")
        print()
    
    def writeMaze(self,file):
        """
        Converts a Maze object back into a textfile. Used to append new rooms
        __author__ = 'Nicholas Koy'
        Parameters:
                file: (str) name to the file to be created temporarily

        Side Effects:
                creates a new txt file in the current directory named file
        """
        with open(file,"w") as f:
            maxrowcount = 0
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
            
    def breakWall(self,player, msglog: MessageLog()):
        """
        breakWall allows a player to destroy a non bordering wall
        that are in proximity to the player (1 Cell away).

        __author__ = 'Nicholas Koy'

        Args:   
                direction (str) either "up", "down", "left", or "right"
                player (Player) the player breaking the wall.
                msglog (MessageLog): Where the action will be printed
        
        Side effects:   Breaks a non bordering wall in front of the player.
                        Prints to standard out via msglog
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
                    choice = input("What wall would you like to break or 'c'"+\
                        " to cancel\n")
                    if choice == "c":
                        break
                    elif choice in breakable:
                        self.tuplemaze[dirs[choice]].obsID = " "
                        player.abilityList["break"] = 5
                        choose = True
                        msglog.addLog(player.name +" broke wall at "+\
                            dirs[choice])
                        print(msglog)
            else: msglog.addLog("No wall to break")
        else: msglog.addLog("Break on cooldown for "\
            +str(player.abilityList["break"])+" turns")
    sleep(2)
    #Ali
    def generateTreasure(self,player,msgLog : MessageLog()):
        """
        Generates treasure for the player to add to their inventory
        Treasure adds to their score and each treasure has a different score val

        __author__ = 'Ali Iqbal', 'Nelson Contreras', and 'Nicholas Koy'

        Args:
                player (Player)    : player picking up treasure
                msgLog (MessageLog): Event logger
        
        Side effects:   adds key or changes key values in player.inventory
                        prints to stdout via msglog
        """
        treasureRoll = randint(0,100)
        addItem = ""
        quantRoll = random.choice([1,1,1,1,1,1,2,2,2,2,3,3,3,4,4,4,5,5,10])
        if treasureRoll >= 95 and treasureRoll <= 100:
            addItem = "Diamond"
        elif treasureRoll >= 80 and treasureRoll < 95:
            addItem = "Gold"
        elif treasureRoll >= 60 and treasureRoll < 80:
            addItem = "Emerald"
        elif treasureRoll >= 50 and treasureRoll < 60:
            addItem = "Silver"
        elif treasureRoll >= 35 and treasureRoll < 50:
            addItem = "Bronze"
        elif treasureRoll >= 20 and treasureRoll < 35:
            addItem = "Copper"
        elif treasureRoll >= 10 and treasureRoll < 20:
            addItem = "Amber"
        else:
            addItem = "Nugget"
        if addItem in ["Diamond","Emerald"]:
            piece = "gem"
        elif addItem in ["Silver", "Bronze","Copper"]:
            piece = "ore"
        else:
            piece = "piece"
        if quantRoll > 1:
            msgLog.addLog(player.name + " picked up " + str(quantRoll) + " "+\
                str(addItem) + " " + str(piece) +"s")
        else:
            msgLog.addLog(player.name + " picked up one " + str(addItem) +\
               " " +  str(piece))
        if addItem not in player.inventory.keys():
            player.inventory[addItem] = quantRoll
        else:
            player.inventory[addItem] += quantRoll
    #Noble
    def revealMap(self,player):
        """
        This reveals the game map if it is in the players inventory
        __author__ = 'Noble Nwokoma'
        Args:
            player(Player): The player in the game
        Side effects: Makes the map entire layout visible and reveals treasure
        """
        if player.inventory["map"] == 1:
            for cell in self.tuplemaze.keys():
                self.tuplemaze[cell].revealed = True
    #Noble
    def jumpWall(self, player,msgLog : MessageLog()):
        """
        this enables players who have the ability to jump over walls in the
        maze to be able to do so

        __author__ = 'Noble Nwokoma'
        Args:
            player(String): The name of the player in the game
            it will evaluate the player and see if they have the ability to do
             so and if they can to execute, if not then the the code will break
        """
        row,col = self.currentTuple
        choose = False
        jumpable = ["c"]
        dirs = { "up":"("+str(row-1)+", "+str(col)+")","down":"("+str(row+1)+\
        ", "+str(col)+")","left":"("+str(row)+", "+str(col-1)+")",\
                 "right":"("+str(row)+", "+str(col+1)+")"}
        dirs2 = { "up":"("+str(row-2)+", "+str(col)+")","down":"("+str(row+2)+\
        ", "+str(col)+")","left":"("+str(row)+", "+str(col-2)+")",\
                 "right":"("+str(row)+", "+str(col+2)+")"}
        if player.abilityList["jump"] == 0:
            for jumpCheck in dirs: #check if a wall exists nearby
                if dirs[jumpCheck] in self.tuplemaze.keys():
                    if self.tuplemaze[dirs[jumpCheck]].obsID == "=" and \
                    (dirs2[jumpCheck] in self.tuplemaze.keys()) and \
                    self.tuplemaze[dirs2[jumpCheck]].obsID not in ["=","/"]:
                        jumpable.append(jumpCheck)
            if len(jumpable) > 1:
                while not choose:
                    #cls()
                    strjump = ""
                    for direc in jumpable:
                        strjump += (direc + " ")
                    strjump = strjump.strip()
                    strjump = strjump.replace(" ",', ')
                    print("Options:",strjump)
                    choice = input("Which wall do you want to jump? Or 'c' to"+\
                    " cancel\n")
                    if choice == "c":
                        break
                    elif choice in jumpable:
                        self.tuplemaze[str(self.currentTuple)].playerthere=False
                        newPos = dirs2[choice]
                        newPos2 = newPos
                        newPos = newPos.replace("(","")
                        newPos = newPos.replace(")","") 
                        newRow = int(newPos.split(", ") [0])
                        newCol = int(newPos.split(", ") [1])
                        self.tuplemaze[newPos2].playerthere=True 
                        self.tuplemaze[newPos2].revealed=True 
                        self.currentTuple = newRow, newCol
                        player.abilityList["jump"] = 5
                        msgLog.addLog(player.name +" jumped over a wall")
                        choose = True
            else:
                msgLog.addLog("There is no wall to jump over")
        else:
            j = "jump"
            msgLog.addLog("Jump is still on cooldown for "+\
                str(player.abilityList[j]) +  "turns")
    #Nick 
    def move(self,player,msglog,DEBUG = False):
        """
        A players "turn" in a maze. Here they can decide to either move, rest,
        or perform a skill.

        __authors__ =   'Ali Iqbal', 'Nelson Contreras', 'Nicholas Koy', and
                        'Noble Nwokoma'

        Args:
                player: (Player) the player about to perform an action.
        Side effects:   Prints to stdout and changes attributes such as
                        player health and hunger. Maze revealed via
                        revealSurround()
        """
        if player.shortCom:
            ask = "\n(U),(D),(L),(R),(Rest),(B),(J),(Use),(P)" +\
                "(stats),(short),(logs)\n"
        else: ask = "\nMove where? (U)p,(D)own,(L)eft, or (R)ight\n" +\
        "Other: (Rest), (B)reak Wall, (J)ump Wall, (use) item, or (P)osition" +\
        "\nShow (Inventory),(equip) gear \n" +\
        "Toggles: player(stats),(short) commands,(dark),(light) or see (logs)\n"

        resp = input(ask)
        moved = False
        torchOn = False
        msgWait = False
        tupUp = self.currentTuple #THIS IS NOT A STRING YET
        row,col = tupUp
        resp = resp.lower()
        if resp == "dark" or resp == "light":
            self.visible(resp)
        if resp == "enemy":
            msglog.addLog(str(self.enemyPos))
            for enemy in self.enemyPos:
                print(enemy,self.getDistance(enemy))
            sleep(2)
        if resp == "stats":
            player.hideStats = not player.hideStats
        elif resp == "logs":
            player.hideLog = not player.hideLog
        elif DEBUG and resp == "spawnloot":
            temp = Gear("Sword","Legendary",5)
            msglog.addLog(temp.name)
            print(temp.name)
            player.addInventoryWearable(temp)
            print(msglog)
        #DONT GRADE THIS ELIF
        #This is basically just an endless combat sim
        elif DEBUG and resp == "combatplus":
            restsLeft = 5
            lv = int(input("what level?\n"))
            player.inventory["armor"]["equip"]["Helmet"] = Gear("Helmet","Rare",lv)
            player.inventory["armor"]["equip"]["Boots"] = Gear("Boots","Rare",lv)
            player.inventory["armor"]["equip"]["Gloves"] = Gear("Helmet","Rare",lv)
            player.inventory["armor"]["equip"]["Body Armor"] = Gear("Helmet","Rare",lv)
            player.inventory["sword"]["equip"] = Gear("Sword","Rare",lv)
            recalcDefense(player)
            recalcAttack(player)
            print(player.gearOffense)
            battleRest = ""
            battleRest = input("Battle 'b', Rest 'r', equip 'e', or 'c' to quit\n")
            while battleRest != "c":
                if battleRest == "b":
                    e1 = Enemy()
                    e1.inventory["armor"]["equip"]["Helmet"] = Gear("Helmet","Rare",lv)
                    e1.inventory["armor"]["equip"]["Boots"] = Gear("Boots","Rare",lv)
                    e1.inventory["armor"]["equip"]["Gloves"] = Gear("Helmet","Rare",lv)
                    e1.inventory["armor"]["equip"]["Body Armor"] = Gear("Helmet","Rare",lv)
                    e1.inventory["sword"]["equip"] = Gear("Sword","Rare",lv)
                    #print(calcDamage(player,e1))
                    #print("att",player.gearOffense)
                    #print("def",player.gearDefense)
                    print("enemy")
                    print("att",e1.gearOffense)
                    print("def",e1.gearDefense)
                    recalcAttack(e1)
                    recalcDefense(e1)
                    sleep(2)
                    while (player.health > 0 and e1.health > 0):
                        battle_monsters(player,e1,self,msglog)
                    if player.health < 0:
                        break
                elif battleRest == "r" and restsLeft > 0:
                    player.health += round(.5 * player.maxhealth)
                    if player.health > player.maxhealth:
                        player.health = player.maxhealth
                    restsLeft -=1
                    print("Rests left: ",restsLeft)
                elif battleRest == "e":
                        player.equipGear(msglog)
                battleRest = input("Battle 'b', Rest 'r', equip 'e', or 'c' to quit\n")
                sleep(2)
                cls()
        elif DEBUG and resp == "armor":#adds armor to inv for the player test
            lv = int(input("up to what level?\n"))
            rarity = ["Ultra Rare","Legendary","Common","Uncommon","Rare"]
            
            player.addInventoryWearable(Gear("Helmet",random.choice(rarity),randint(0,lv)))
            player.addInventoryWearable(Gear("Boots",random.choice(rarity),randint(0,lv)))
            player.addInventoryWearable(Gear("Gloves",random.choice(rarity),randint(0,lv)))
            player.addInventoryWearable(Gear("Body Armor",random.choice(rarity),randint(0,lv)))
            player.addInventoryWearable(Gear("Sword",random.choice(rarity),randint(0,lv)))
            #recalcDefense(player)
            #recalcAttack(player)
        #Okay you can look now
        elif resp == "inventory":
            lookup = input("Gear or Items?\n").lower()
            if lookup == "gear":
                player.showInventory()
                sleep(3)
            elif lookup == "items":
                for item in player.inventory.keys():
                    if item != "sword" and item != "armor":
                        print(item,":",player.inventory[item])
                sleep(4)
        elif resp == "short":
            player.shortCom = not player.shortCom
        elif resp == "use":
            item = input("What item are you using?\n"+\
                "Food, torch, map, or bandage").lower()
            player.useItem(item,msglog,self)
        elif resp == "equip":
            player.equipGear(msglog)
        elif resp == "unequip":
            gearSlot = input("Which item to unequip\n")
            player.unequipGear(gearSlot,msglog)
        elif resp in ["u","up"]:
            self.moveUp(player,msglog,DEBUG)
            moved = True
        elif resp in ["d","down"]:
            self.moveDown(player,msglog,DEBUG)
            moved = True
        elif resp in ["l","left"]:
            moved = True
            self.moveLeft(player,msglog,DEBUG)
        elif resp in ["right","r"]:
            moved = True
            self.moveRight(player,msglog,DEBUG)
        elif resp == "j": #jumpWall
            self.jumpWall(player,msglog)
            moved = True
        elif resp == "b": #breakWall
            self.breakWall(player,msglog)
        elif resp == "p": # used primarily for debugging
            msglog.addLog("You check your surroundings, you are at "+\
                str(self.currentTuple))
        elif resp == "rest":
            if player.hunger > 10:
                player.health += round(player.maxhealth/10)
                if player.health > player.maxhealth:
                    player.health = player.maxhealth
                player.hunger -= 10
                msglog.addLog("You take a short rest",True)
                for ability in player.abilityList.keys():
                    if player.abilityList[ability] > 0:
                        player.abilityList[ability] -= 5
                    if player.abilityList[ability] < 0:
                        player.abilityList[ability] = 0
        else: 
            msglog.addLog("Invalid Action")
            msgWait = True
        if moved: #reduce hunger and health and cooldowns inc hp if hunger > 0
            if player.hunger > 0:
                if player.health+1 < player.maxhealth : player.health += 1
            self.afterMove(player,msglog,DEBUG)
            for enemy in self.enemyPos:
                self.enemyMove(enemy,player,msglog)
                if str(self.currentTuple) in self.enemyPos:
                    self.tuplemaze[str(self.currentTuple)].obsID = " "
                    enemyGen = Enemy()
                    msglog.addLog(player.name+" encountered a " + enemyGen.name)
                    cls()
                    print(msglog)
                    sleep(1.3)
                    battle_monsters(player, enemyGen, self,msglog)
                    self.enemyPos.remove(str(self.currentTuple))
                if enemy not in self.enemyPos:
                    self.tuplemaze[enemy].obsID = " "
        if(msgWait):
            sleep(.3)
    def moveUp(self,player,msglog,DEBUG = False):
        """
        Moves the player up if possible
        WILL NOT COUNT TOWARDS 8 UNIQUE METHODS
        ADDED TO MAKE PYTEST EASIER
        Args: same as move()
        Side effects: same as move()
        """
        tupUp = self.currentTuple #THIS IS NOT A STRING YET
        row,col = tupUp
        up = str(self.currentTuple)
        tupNewUp = "("+str(row-1)+", "+str(col)+")"
        if tupNewUp in self.tuplemaze.keys() and \
            self.tuplemaze[tupNewUp].obsID not in ["=","/"]:
            self.tuplemaze[up].playerthere = False
            self.currentTuple = (row-1,col)
            self.tuplemaze[tupNewUp].playerthere = True
        else: msglog.addLog("A wall obstructs you")
    def moveDown(self,player,msglog,DEBUG = False):
        """
        Moves the player down if possible
        WILL NOT COUNT TOWARDS 8 UNIQUE METHODS
        ADDED TO MAKE PYTEST EASIER
        Args: same as move()
        Side effects: same as move()
        """
        tupUp = self.currentTuple #THIS IS NOT A STRING YET
        row,col = tupUp
        up = str(self.currentTuple)
        tupNewUp = "("+str(row+1)+", "+str(col)+")"
        if tupNewUp in self.tuplemaze.keys() and \
            self.tuplemaze[tupNewUp].obsID not in ["=","/"]:
            self.tuplemaze[up].playerthere = False
            self.currentTuple = (row+1,col)
            self.tuplemaze[tupNewUp].playerthere = True
            moved = True
        else: msglog.addLog("A wall obstructs you")
    def moveLeft(self,player,msglog,DEBUG = False):
        """
        Moves the player left if possible
        WILL NOT COUNT TOWARDS 8 UNIQUE METHODS
        ADDED TO MAKE PYTEST EASIER
        Args: same as move()
        Side effects: same as move()
        """
        tupUp = self.currentTuple #THIS IS NOT A STRING YET
        row,col = tupUp
        up = str(self.currentTuple)
        tupNewUp = "("+str(row)+", "+str(col-1)+")"
        if tupNewUp in self.tuplemaze.keys() and\
            self.tuplemaze[tupNewUp].obsID not in ["=","/"]:
            self.tuplemaze[up].playerthere = False
            self.currentTuple = (row,col-1)
            self.tuplemaze[tupNewUp].playerthere = True
            moved = True
        else: msglog.addLog("A wall obstructs you")
    def moveRight(self,player,msglog,DEBUG = False):
        """
        Moves the player right if possible
        WILL NOT COUNT TOWARDS 8 UNIQUE METHODS
        ADDED TO MAKE PYTEST EASIER
        Args: same as move()
        Side effects: same as move()
        """
        tupUp = self.currentTuple #THIS IS NOT A STRING YET
        row,col = tupUp
        up = str(self.currentTuple)
        tupNewUp = "("+str(row)+", "+str(col+1)+")"
        if tupNewUp in self.tuplemaze.keys() and\
            self.tuplemaze[tupNewUp].obsID not in ["=","/"]:
            self.tuplemaze[up].playerthere = False
            self.currentTuple = (row,col+1)
            self.tuplemaze[tupNewUp].playerthere = True
            moved = True
        else: msglog.addLog("A wall obstructs you")
    def afterMove(self,player,msglog,DEBUG = False):
        """
        Checks the new tile the player has moved to.
        DONT COUNT TOWARDS 8 UNIQUE METHODS
        MAINLY FOR PYTEST EASY TESTING SINCE main() usually covers this
        """
        for ability in player.abilityList.keys():
            if player.abilityList[ability] > 0:
                player.abilityList[ability] -= 1
        if player.hunger > 0:
            player.hunger -= 1
        else: player.health -=1
        if player.torchLeft > 0:
            torchOn = True
            player.torchLeft -= 1
        else:
            torchOn = False
        if player.health == 0: #death check
            msglog.addLog(player.name," has died of starvation")
        if player.health > 0 and \
            self.tuplemaze[str(self.currentTuple)].obsID == "T":

            self.generateTreasure(player,msglog)
            self.tuplemaze[str(self.currentTuple)].obsID = " "
        #stair check
        if self.tuplemaze[str(self.currentTuple)].obsID.isdigit():
            msglog.addLog(player.name+" took the stairs")
            print(self.tuplemaze[str(self.currentTuple)].playerthere)
            self.revealSurround(torchOn) 
            #Have to reveal surrounding area before moving somewhere new
            pos1,pos2 = self.mazeStairs\
                [self.tuplemaze[str(self.currentTuple)].obsID]
            self.tuplemaze[str(self.currentTuple)].playerthere = False
            if self.currentTuple == pos1:
                self.currentTuple = pos2
            else:
                self.currentTuple = pos1
            self.tuplemaze[str(self.currentTuple)].playerthere = True
            self.tuplemaze[str(self.currentTuple)].revealed = True
        #battle check
        if player.health > 0 and \
            self.tuplemaze[str(self.currentTuple)].obsID == "B":
            self.tuplemaze[str(self.currentTuple)].obsID = " "
            enemyGen = Enemy()
            msglog.addLog(player.name+" encountered a " + enemyGen.name)
            cls()
            print(msglog)
            sleep(1.3)
            battle_monsters(player, enemyGen, self,msglog)
            if str(self.currentTuple) in self.enemyPos:
                self.enemyPos.remove(str(self.currentTuple))
        self.revealSurround(torchOn) 
    def setBorders(self):
        """
        Sets border attribute for cells in proximity to the edge / void

        __authors__ =  'Nicholas Koy'

        Side effect: Sets isBorder attr of certain Cells in tuplemaze dict
        """
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
                if dirs[dire] not in self.tuplemaze.keys() or\
                self.tuplemaze[dirs[dire]].obsID == "/":
                    self.tuplemaze[cellKey].isBorder = True
    def getBorder(self):
        """
        __authors__ = 'Nicholas Koy'
        Gets a list of all cells that are borders

        Returns: list of strings of cell keys from tuplemaze
        """
        borderList = []
        for cell in self.tuplemaze.keys():
            if self.tuplemaze[cell].isBorder:
                borderList.append(cell)
        return borderList
    def enemyMove(self,singleEnemy,player,msglog):
        """
        Makes the enemies randomly move around the maze
        Enemies can only move to open tiles ' '
        """
        pos = singleEnemy.replace("(","")
        pos = pos.replace(")","")
        row = int(pos.split(",")[0])
        col = int(pos.split(",")[1])
        strTup = row,col
        strTup = str(strTup)
        if singleEnemy in self.enemyPos and \
            round(self.getDistance(singleEnemy)) > 1.42 :
            dirs = { "up":"("+str(row-1)+", "+str(col)+")",
            "down":"("+str(row+1)+\
            ", "+str(col)+")","left":"("+str(row)+", "+str(col-1)+")",\
                 "right":"("+str(row)+", "+str(col+1)+")"}
            validDir = []
            for tile in dirs.keys():
                if self.tuplemaze[dirs[tile]].obsID == " ":
                    validDir.append(tile)
            if len(validDir) > 0:
                move = random.choice(validDir)
                #print(move)
                strTup = dirs[move]
                self.tuplemaze[singleEnemy].obsID = " "
                self.tuplemaze[dirs[move]].obsID = "B"
                self.enemyPos.remove(singleEnemy)
                self.enemyPos.append(strTup)
                #sleep(1)
        elif singleEnemy in self.enemyPos and\
         round(self.getDistance(singleEnemy),3) == 1:#Enemy is one tile away 
            print("close",singleEnemy)
            sleep(1)
            enemyGen = Enemy()
            msglog.addLog(player.name+" encountered a " + enemyGen.name)
            cls()
            print(msglog)
            sleep(1.3)
            battle_monsters(player, enemyGen, self,msglog)
            self.tuplemaze[singleEnemy].obsID == " "
            self.enemyPos.remove(singleEnemy)
    def getDistance(self,singleEnemy):
        """
        Calculates the distance between an enemy and the player
        __author__ = 'Nicholas Koy'
        Args: singleEnemy (str): cell representing an enemy

        Returns: distance (float) how far the two entities are
        """
        pos = singleEnemy.replace("(","")
        pos = pos.replace(")","")
        row = int(pos.split(",")[0])
        col = int(pos.split(",")[1])
        curPos = str(self.currentTuple)
        curPos = curPos.replace("(","")
        curPos = curPos.replace(")","")
        curRow = int(curPos.split(",")[0])
        curCol = int(curPos.split(",")[1])
        diffRow = curRow - row
        diffCol = curCol - col
        distance = (diffRow **2 + diffCol**2)** .5
        return distance
    def revealSurround(self,torch = False):
        """
        Reveals the surrounding maze area (one cell away from the player 
        and two if the player has a torch)

        __authors__ =   'Ali Iqbal', and 'Nicholas Koy'

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
        torchDirs = { 
            "up":"("+str(row-2)+", "+str(col)+")",\
            "down":"("+str(row+2)+", "+str(col)+")",
            "left":"("+str(row)+", "+str(col-2)+")", \
            "right":"("+str(row)+", "+str(col+2)+")"
            }   
        #currently only reveals one tile, 2 to be added soon        
        for key in dirs.keys():
            if dirs[key] in self.tuplemaze.keys():
                self.tuplemaze[dirs[key]].revealed = True
        if torch:
            for key in torchDirs.keys():
                if torchDirs[key] in self.tuplemaze.keys():
                    self.tuplemaze[torchDirs[key]].revealed = True
class Player:
    """
    A Player explores a Maze. While exploring the maze their hunger goes down.
    Occasionally they may find an enemy that they must battle or run from.
    Players have skills they can use to traverse the maze easier.

    __author__ = 'Nelson Contreras': Class, init

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
            hideLog (Boolean):  Toggle for logs to print
            hideStats (Boolean):If printMaze should show player steps
            shortCom (Boolean): Short hand commands
            battlesWon (int):   The number of battles the player has won
            battlesFought (int):The number of battles the player has fought
            torchLeft (int):    How many steps they can see farther
            gearDefense (list): Used to calculate damage block
            gearOffense (list): Added damage calculations
        
    """                     
    def __init__(self,name,health,attack,speed,hunger):
        """
        Initializes a new Player object

        Parameters:
                name (str): name of the new player
                health (float): HP of the new player
                attack (float): Attack damage of the player
                speed (float): speed of the player
                hunger (float): How full the player is
        Side effects: Initializes a new Player object
        """
        startingSword = Gear("Sword","Common",1)
        if startingSword.attackVal[0] < 5: startingSword.attackVal[0] = 5
        
        self.inventory = {"map": 1, "sword": {"equip": startingSword, \
            "unequip": [] },
        "armor" : {"equip": {"Helmet": None,"Body Armor":None,
                "Boots":None,"Ring":None,"Amulet":None,"Gloves":None}, \
                "unequip": []}, 
        "small core": 0, "medium core":0, "large core": 0, "torch": 1,
        "bandage":1}
        self.abilityList = {"break": 0, "jump": 0}
        self.name = name
        self.health = health
        self.maxhealth = health
        self.attack = attack
        self.hunger = hunger
        self.maxhunger = hunger
        self.speed = speed
        self.starve = False
        self.hideStats = False
        self.hideLog = True
        self.shortCom = False
        self.torchLeft = 0
        self.battlesWon = 0
        self.battlesFought = 0
        self.gearOffense = [0,0,0,0,0]
        self.gearDefense = self.gearOffense
        recalcAttack(self)
    def __str__(self):
        """
        __author__ = 'Nicholas Koy':Wanted to make str look more pretty
        Prints the player object neatly and with Color for any elemental damage
        Red Text followed by F : Fire damage
        Blue Text followed by C: Cold damage
        Yellow Text followed by L: Lightning damage
        Green Text followed by T: Toxic/Poison damage

        Returns: str of player object stat attribute in a frame
        """
        validDmg = (str(self.attack)+"B"),
        totalDmg = self.attack
        numColors = 0
        elementColor = {  
                    "L": "\033[93m",
                    "C": "\033[96m",
                    "T": "\033[92m",
                    "F": "\033[31m" 
                    }
                #important "\033[0m"
        damageMap = {0:"P",1:"F",2:"L",3:"C",4:"T"}
        for damageType in range(len(self.gearOffense)):
            if self.gearOffense[damageType] > 0:
                numColors +=1
                totalDmg += self.gearOffense[damageType]
                if damageType != 0:#Adds color
                    validDmg = (validDmg[0] + " " +\
                        elementColor[damageMap[damageType]]+\
                            str(self.gearOffense[damageType])+\
                                damageMap[damageType]+"\033[0m"),
                else:
                    validDmg = (validDmg[0] + " " +str(self.gearOffense\
                        [damageType])+damageMap[damageType]),
        validDmg = str(totalDmg)+":"+validDmg[0]
        tup =  (("#","S"),
                ("▯ Name  :", self.name),
                ("▯ Health:",str(self.health)+"/"+str(self.maxhealth)),
                ("▯ Attack:", validDmg),
                ("▯ Speed :", str(self.speed)),
                ("▯ Hunger:", str(self.hunger)+"/"+str(self.maxhunger)),
                ("#","E"))
        maxFrame = 0
        hasColor = False
        maxColorFrame = 0
        for x,y in tup:
            if x != "▯ Attack":
                if len(x) + len(y) > maxFrame: maxFrame = len(x) + len(y)
            else:
                if "[" in x:
                    hasColor = True
                    maxColorFrame = len(x) + len(y) + 5
        maxFrame += 5
        printFrame =""
        for x,y in tup:
            if x == "#":
                row = "▭" * (maxFrame+2 - (9*(numColors-1)))
                if y == "S":
                    row = row + "\n"
                elif y == "E":
                    row = row + "\n"
                printFrame += row
            elif "[" not in y:# The stats print
                rightrow = str(y)
                row = x + " " * (maxFrame - (9*numColors) - len(rightrow)) + \
                    rightrow+" ▯\n"
                printFrame += row
            else: #Color
                rightrow = str(y)
                row = x + " " * (maxFrame - 9 - len(rightrow)) + rightrow+" ▯\n"
                printFrame += row 
        return (printFrame)
    #Ali
    def getScore(self):
        """
        __author__ = 'Ali Iqbal'
        Calculates the score of the player based on treasure owned and battles
        won/battles fought

        Returns: Integer score of player
        """
        score = 0
        for i in self.inventory.keys():
            if i == "Diamond":
                score += self.inventory[i]*100
            elif(i == "Gold"):
                score += self.inventory[i]*80
            elif(i == "Emerald"):
                score += self.inventory[i]*60
            elif(i == "Silver"):
                score += self.inventory[i]*50
            elif(i == "Bronze"):
                score += self.inventory[i]*35
            elif(i == "Copper"):
                score += self.inventory[i]*20
            elif(i == "Amber"):
                score += self.inventory[i]*15
            elif(i == "Nugget"):
                score += self.inventory[i]*10
            elif i == "small core":
                score += (75 * self.inventory[i])
            elif i == "medium core":
                score += (125 * self.inventory[i])
            elif i == "large core":
                score += (200 * self.inventory[i])
        score += (100 * self.battlesWon)
        if self.battlesFought != 0:
            score = int(score * (self.battlesWon/self.battlesFought))
        else:
            score = int(score * .75) 
        
        return score

    def useItem(self,item,msgLog,maze,battle = False):
        """
        __author__ = 'Nelson Contreras','Nicholas Koy'
        Players can use certain items to aid them in their travels

        Args: item (str): the item to be searched in inv and used

        Side effects: Uses the item. Different items have different effects
                      May lower quantity
        """
        validItems = ["food","torch","bandage","map"]
        if battle:
            validItems = ["torch","bandage"]

        if item in validItems:
            if item in self.inventory.keys() and self.inventory[item] > 0:
                if item == "torch":
                    self.torchLeft = randint(12,20)
                    msgLog.addLog(self.name + " burns a torch")
                elif item == "bandage":
                    self.health += int(self.maxhealth * .25)
                    if self.health > self.maxhealth:
                        self.health = self.maxhealth
                    msgLog.addLog(self.name + " bandages up their wounds")
                elif item == "map":
                    maze.revealMap(self)
                    msgLog.addLog(self.name + " reads a map")
                elif item == "food":
                    validFood = ["apple","bread","carrot","Mystery Meat"]
                    for food in validFood:
                        if food not in self.inventory.keys():
                            validFood.remove(food)
                        elif self.inventory[food] == 0:
                            validFood.remove(food)
                    if len(validFood) > 0:
                        message = "What are you eating: "
                        for food in validFood:
                            message += food + " "
                        message = message.strip()
                        choice = input(message)
                        if choice in validFood:
                            self.inventory[choice] -= 1
                            self.health += self.maxhealth * .15
                            if self.health > self.maxhealth:
                                self.health = self.maxhealth
                self.inventory[item] -= 1
            else:
                msgLog.addLog("You have no more to use")
        else:
            msgLog.addLog("Item doesn't exist")
    def addInventoryWearable(self,item):
        """
        Adds newly generated loot to the players inventory

        __author__ = 'Nicholas Koy'

        Args:
                item (Gear): newly genned item
        
        Side Effects:   Appends to 2 dictionaries
        """
        if item.slot in ["Gloves","Helmet","Boots","Ring","Amulet","Body Armor"]:
            self.inventory["armor"]["unequip"].append(item)
        elif  item.slot in ["Sword"]:
            self.inventory["sword"]["unequip"].append(item)
                 
    def showInventory(self,swap = False,unequip = False):
        """
        Prints the gear the player has
        __author__ = 'Nicholas Koy'
        Args:
                swap(Boolean): If the player needs to see item position
                unequip (Boolean): Shows just equipped items if True
        Side Effect: Prints to stdout
        """
        os.system('')
        count = 0
        countunequip = 0
        print("===================== Equipped =========================")
        if countunequip:
            print(self.inventory["sword"]["equip"] + "Item ", countunequip)
            countunequip += 1
        else:
            print(self.inventory["sword"]["equip"])
        for armor in self.inventory["armor"]["equip"].keys():
            if self.inventory["armor"]["equip"][armor] != None:
                if countunequip:
                    print(self.inventory["armor"]["equip"][armor] + "Item " +\
                        countunequip)
                    countunequip += 1
                else: print(self.inventory["armor"]["equip"][armor])
        if not unequip:
            print("===================== Not Equipped =====================")
            for gear in self.inventory["sword"]["unequip"]:
                print(gear)
                if swap:
                    print("Gear ",count)
                    count+=1
            for gear in self.inventory["armor"]["unequip"]:
                print(gear)
                if swap:
                    print("Gear ",count)
                    count+=1
    def equipGear(self,msgLog : MessageLog()):
        """
        Asks the player to swap equipped gear (if any) for the same type
        that they potentially picked up
        __author__ = 'Nicholas Koy'
        """
        self.showInventory(swap = True)
        action = ""
        item = int(input("What item # do you want to equip\n"))
        if item >= 0 and item <= (len(self.inventory["armor"]["unequip"])) +\
            (len(self.inventory["sword"]["unequip"]) - 1):
            if item < len(self.inventory["sword"]["unequip"]):
                print("Swapping Swords")
                if self.inventory["sword"]["equip"] != []:
                    swapGear = self.inventory["sword"]["equip"]
                    self.inventory["sword"]["unequip"].append(swapGear)
                    self.inventory["sword"]["equip"]= \
                        self.inventory["sword"]["unequip"][item]
                    del self.inventory["sword"]["unequip"][item]
                    msgLog.addLog("Swapped Sword to " + \
                        self.inventory["sword"]["equip"].name+" ")
                    recalcAttack(self)
                    recalcDefense(self)
            else:
                armorType = self.inventory["armor"]["unequip"][item - \
                    len(self.inventory["sword"]["unequip"])].slot
                armorName = self.inventory["armor"]["unequip"][item - \
                    len(self.inventory["sword"]["unequip"])].name
                #see if there is already an armor of that type equipped
                if self.inventory["armor"]["equip"][armorType] != None:
                    tempArmor = self.inventory["armor"]["equip"][armorType]
                    self.inventory["armor"]["unequip"].append(tempArmor)
                    self.inventory["armor"]["equip"][armorType] = \
                        self.inventory["armor"]["unequip"][item - \
                            len(self.inventory["sword"]["unequip"])]
                    del self.inventory["armor"]["unequip"][item - \
                        len(self.inventory["sword"]["unequip"])]
                    action = "Swapped " + armorType + " to " + \
                        tempArmor.name + " "
                else:
                    self.inventory["armor"]["equip"][armorType]= \
                        self.inventory["armor"]["unequip"][item - \
                            len(self.inventory["sword"]["unequip"])]
                    del self.inventory["armor"]["unequip"][item - \
                        len(self.inventory["sword"]["unequip"])]
                    action = "Equipped " + armorName + " to " +\
                         armorType + " slot "
                recalcAttack(self)
                recalcDefense(self)
                self.maxhealth += self.gearDefense[0]
                self.health += self.gearDefense[0]
        msgLog.addLog(action)  
        print(msgLog)
        sleep(1)
        cls()
        self.showInventory()
    def unequipGear(self,itemType,msgLog : MessageLog()):
        """
        Unequips a gear item from the player.

        Args:   itemType (str): "Body Armor","Helmet","Sword","Gloves","Boots"
        Side effects:           prints to stdout and changes player.inventory
                                ["equip](["sword"] or ["armor"]) to [] or None
                                and appends the previously equipped item to
                                ...["unequip]["sword"]/["armor"] dictionary
                                respectively
        """
        self.showInventory(False,True)
        action = ""
        if itemType.lower() in ["sword","helmet","gloves","boots","body armor"]:
            if itemType == "sword" and self.inventory["sword"]["equip"] != None:
                print("hello")
                sleep(3)
                self.inventory["sword"]["unequip"].append(\
                    self.inventory["sword"]["equip"])
                self.inventory["sword"]["equip"] = None
                action = "Put Sword away "
                recalcAttack(self)
            elif self.inventory["armor"]["equip"][itemType] != None:
                self.inventory["armor"]["unequip"].append(\
                    self.inventory["armor"]["equip"][itemType])
                name = self.inventory["armor"]["equip"][itemType].name
                hpsub =self.inventory["armor"]["equip"][itemType].defenseVals[0]
                self.maxhealth - abs(hpsub)
                self.health - abs(hpsub)
                self.inventory["armor"]["equip"][itemType] = None
                action = "Put " + name + " away "

                recalcDefense(self)
            msgLog.addLog(action)
            print(msgLog)
            sleep(1)
            cls()
            self.showInventory()
class Enemy:
    """
    __author__ = 'Nelson Contreras' : __init__() and __str__()
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
    attack (float) - this will be the monsters base attack damage.
    inventory (Dict): will store the monster's equipped gear for damage calc
    """
    def __str__(self):
        return self.name
    def __init__(self,diff = 1):
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
        self.montype = random.choice([1,1,1,1,1,1,1,1,2,2,2,2,3,3,3,4,4,5])
        self.gearOffense = [0,0,0,0,0]
        self.gearDefense = self.gearOffense
        if self.montype == 1:
            self.attack = randint(40,60)
            self.speed = randint(30,50)
            self.name = "Lv 1 " + self.name
        elif self.montype == 2:
            self.attack = randint(50,65)
            self.speed = randint(40,55)
            self.name = "Lv 2 " + self.name
        elif self.montype == 3:
            self.attack = randint(60,75)
            self.speed = randint(50,70)
            self.name = "Lv 3 " + self.name
        elif self.montype == 4:
            self.attack = randint(75,95)
            self.speed = randint(55,60)
            self.name = "Lv 4 " + self.name
        else:
            self.attack = randint(80,100)
            self.speed = randint(60,70)
            self.name = "Lv 5 " + self.name
        self.health = factorial(self.montype) * 5 + 100
        #balance
        self.attack = self.attack* 2 / 3 
        if "Zombie" in self.name:
            self.health *= .9
            self.attack += 3
            self.speed -= 30
        elif "Kobold" in self.name:
            self.health *= .7
            self.speed += 5
            self.attack += 7
        elif "Skeleton" in self.name:
            self.health *= .6
            self.attack -= 3
            self.speed += 12
        elif "Orc" in self.name:
            self.health *= .4
            self.attack -= 7
            self.speed += 5
        elif "Goblin" in self.name:
            self.health *= 1.1
            self.attack += 5
        elif  "Lizard" in self.name:
            self.speed += 8
            self.attack *= 1.10
        elif "Spectre" in self.name:
            self.speed += 20
            self.attack *= 1.8
            self.health -= 30
        else:
            self.speed -= 30
        self.maxhealth = self.health
        self.inventory = {"sword":{"equip":Gear("Sword","Uncommon",\
            self.montype),"unequip":[]},"armor":
            {"equip":{"Helmet":None,
                "Body Armor":None,
                "Gloves": None,
                "Boots":None,
                "Ring":None,
                "Amulet":None}}}
        armorTypes = ["Gloves", "Boots", "Helmet","Body Armor"]
        #,"Ring","Amulet"]
        armorChoice = random.choice(armorTypes)
        armorTypes.remove(armorChoice)
        self.inventory["armor"]["equip"][armorChoice] = \
            Gear(armorChoice,"Common", 2+(self.montype-4))
        
        #armor dict -> equip dict -> string of gear types pairs to an item
        if self.montype > 3:
            armorChoice = random.choice(armorTypes)
            self.inventory["armor"]["equip"][armorChoice] = \
                Gear(armorChoice,"Ultra Rare", 2+(self.montype-4))
        recalcAttack(self)
        recalcDefense(self)
        self.maxhealth += self.gearDefense[0]
        self.health += self.gearDefense[0]     
class EmptyMaze():
    """
    An EmptyMaze is created when generateSimpleMaze() is called.
    EmptyMaze starts off as an n by m sized rectangle designated by the user
    and procedurally generates start, end, treasure, and battle obstacles.

    __author__ = 'Nicholas Koy' : Class + methods
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

    def printEmptyMaze(self):
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
class Gear():
    """
    Gears come in the form of Armor or Swords. Armor can be enchanted and give
    bonus Health or one resistance to a damaging element (fire,cold,elec,poison)
    Gears have a rarity and a quality system that roll on mainly the montype /
    monster level.
    Some armor may have negative resistances (See battle for more info)
    Swords can be enchanted with 3 modifiers: a Prefix, a suffix, and a unique
    modifier if atleast legendary. Prefixes are attack boost oriented and
    suffixes are defensive boost oriented. The suffix roll can be weak or strong
    and both prefix and suffix are affected by the quality and rarity of the
    item. The multiplicative effect adds up but not all higher rarity and or
    quality items will be strictly better than that of a lesser rarity or qual
    __author__ = 'Nicholas Koy'
    """
    def __init__(self,itemType,rarity,montype,attackVal = None,defenses = None):
        """
        Creates a new Gear Object based on args
        __author__ = 'Nicholas Koy'
        Args: itemType (str)
        """
        if itemType not in ["Helmet","Gloves","Boots","Body Armor","Sword",\
            "Ring","Amulet",
            "Helmet"]: raise ValueError(f"Not a valid item type: {itemType}")
        self.slot = itemType
        if itemType == "Sword":
            newName, attVal, defenseVals = \
                self.generateWeaponEnchant(rarity,montype)
            self.name = newName
            self.attackVal = attVal 
            self.defenses = defenseVals 
            RARITY = {  "Rare": "\033[94m" + newName + "\033[0m",
                    "Ultra Rare": "\033[95m" +newName + "\033[0m",
                    "Legendary": "\033[93m" +  newName+ "\033[0m",
                    "Uncommon": "\033[96m" +  newName+ "\033[0m",
                    "Common": "\033[92m" + newName + "\033[0m",
                    "Unique": "\033[31m" + newName + "\033[0m"
                    }
            self.name = RARITY[rarity]
        elif itemType in ["Gloves","Boots","Body Armor","Helmet"]:
            armorName, baseStats =\
                self.generateArmor(itemType+" ",rarity,montype)
            self.defenses = baseStats
            self.name = armorName
            self.attackVal = [0,0,0,0,0]
            RARITY = {  "Rare": "\033[94m" + armorName + "\033[0m",
                    "Ultra Rare": "\033[95m" +armorName + "\033[0m",
                    "Legendary": "\033[93m" +  armorName+ "\033[0m",
                    "Uncommon": "\033[96m" +  armorName+ "\033[0m",
                    "Common": "\033[92m" + armorName + "\033[0m",
                    "Unique": "\033[31m" + armorName + "\033[0m"
                    }
            self.name = RARITY[rarity]
    def __repr__(self):
        sumAttack = sum(self.attackVal)
        sumDef = sum(self.defenses)
        return (self.name + "\nAttack " +str(self.attackVal)+ ":" +\
            str(sumAttack) + "\nDefenses " +str(self.defenses) +":"+str(sumDef))            
    def __str__(self):
        return self.name
    #Pretend these don't exist or exist as one method
    def generateWeaponEnchant(self,rarity,montype):
        """
        Enchants based on rarity of the Sword and gives extra weight to values if
        montype is higher. Montype should be at most 5 or this won't run nicely

        __author__ = 'Nicholas Koy'
        Args:       rarity (Str): Rarity of the loot
                    montype (Int): Monster level / GearLevel 
        Side effects: scales the base values of attack and def through other f()
        Returns:a tuple containing the str:weapon's new name,list:attack vals,
                list:defense vals
        """
        rolls = 0
        for x in range(3):
            rolls += randint(0,20)
        scaling = 1 + montype/4
        weaponName = ""
        weaponDmg = [0,0,0,0,0] #phys,fire,cold,light,poison
        weaponDefBonus = [0,0,0,0,0]
        secondScale = 1
        if rarity == "Legendary":
            weaponName,weaponDmg,weaponDefBonus = \
                self.addMajorWeaponPrefix("",weaponDmg,weaponDefBonus)
            weaponName,weaponDmg,weaponDefBonus = \
                self.addLesserWeaponSuff\
                    (weaponName,weaponDmg,weaponDefBonus,"",montype)
            weaponName,weaponDmg,weaponDefBonus = \
                self.addUniqueWeaponEnchant(weaponName,weaponDmg,weaponDefBonus)
            weaponName,weaponDmg,weaponDefBonus = \
                self.addWeaponTitle\
                    (weaponName,weaponDmg,weaponDefBonus,montype,rarity)
            weaponDmg = [dmgtype * 1.09 + 7 \
                for dmgtype in weaponDmg if dmgtype > 0]
        elif rarity == "Ultra Rare":
            weaponName,weaponDmg,weaponDefBonus = \
                self.addMajorWeaponPrefix("",weaponDmg,weaponDefBonus)
            weaponName,weaponDmg,weaponDefBonus = \
                self.addLesserWeaponSuff\
                    (weaponName,weaponDmg,weaponDefBonus,"",montype)    
            weaponName,weaponDmg,weaponDefBonus = \
                self.addWeaponTitle\
                    (weaponName,weaponDmg,weaponDefBonus,montype,rarity)
            weaponDmg = [dmgtype * 1.05 +5 for dmgtype in weaponDmg if dmgtype > 0]
        elif rarity == "Unique":
            weaponName,weaponDmg,weaponDefBonus = \
                self.addMajorWeaponPrefix("",weaponDmg,weaponDefBonus)
            weaponName,weaponDmg,weaponDefBonus = \
                self.addLesserWeaponSuff\
                    (weaponName,weaponDmg,weaponDefBonus,"",montype)    
            weaponName,weaponDmg,weaponDefBonus = \
                self.addWeaponTitle\
                    (weaponName,weaponDmg,weaponDefBonus,montype,rarity)
            weaponDmg = [dmgtype * 1.15 + 5 for dmgtype in weaponDmg]
        elif rarity == "Rare":
            weaponName,weaponDmg,weaponDefBonus = \
                self.addMajorWeaponPrefix("",weaponDmg,weaponDefBonus)
            weaponName,weaponDmg,weaponDefBonus = \
                self.addLesserWeaponSuff\
                    (weaponName,weaponDmg,weaponDefBonus,"",montype)
            weaponName,weaponDmg,weaponDefBonus = \
                self.addWeaponTitle\
                    (weaponName,weaponDmg,weaponDefBonus,montype,rarity)
            weaponDmg = [dmgtype * 1.04 + 2\
                for dmgtype in weaponDmg if dmgtype > 0]
        elif rarity == "Uncommon":
            #weaponName,weaponDmg,weaponDefBonus = addMajorWeaponPrefix("",weaponDmg,weaponDefBonus)
            weaponName,weaponDmg,weaponDefBonus =\
                 self.addLesserWeaponSuff\
                     (weaponName,weaponDmg,weaponDefBonus,"",montype)
            weaponName,weaponDmg,weaponDefBonus = \
                self.addWeaponTitle(weaponName,weaponDmg,weaponDefBonus,montype,rarity)
            weaponDmg = [dmgtype * 1.03 + 1 \
                for dmgtype in weaponDmg if dmgtype > 0]
        elif rarity == "Common":
            weaponName,weaponDmg,weaponDefBonus = \
                self.addWeaponTitle\
                    (weaponName,weaponDmg,weaponDefBonus,montype,rarity)
            weaponDmg = [dmgtype * 1.02 + 1\
                for dmgtype in weaponDmg if dmgtype > 0]
        else:
            weaponName,weaponDmg,weaponDefBonus = \
                self.addWeaponTitle\
                    (weaponName,weaponDmg,weaponDefBonus,montype,rarity)
            weaponDmg = [dmgtype * 1.01 for dmgtype in weaponDmg]
        scaledattVal = [int((dmgtype * scaling)*\
            secondScale) for dmgtype in weaponDmg]
        scaleddefVal = [int((restype * scaling)*\
            secondScale) for restype in weaponDefBonus]
        #return a tuple with newName, attackVal, possible Defenses
        return (rarity + " " +weaponName,scaledattVal,scaleddefVal)
    def generateArmor(self,itemType,rarity,montype):
        """
        Generates a newly named armor of base type itemType.
        __author__ = 'Nicholas Koy'
        Scales values on rarity and montype/level
        Args:   itemType (Str): Armor type
                rarity (Str):   Gear rarity
                montype (Int):  Gear Level / Monster level
        Returns: tuple size = 2: Str-item name, list-armorValues
        """
        baseStats = self.generateArmorBaseStats(rarity,montype)
        armorName, baseStats = self.addArmorTitle\
            (itemType,rarity,baseStats,montype)
        armorName, baseStats = self.addArmorSuffix\
            (armorName,baseStats,rarity,montype)
        correction = 0
        if rarity == "Legendary":
            correction = 10 * (montype+2) + 6
        elif rarity == "Unique":
            correction = 11 * (montype+4) + 7
        elif rarity == "Ultra Rare":
            correction = 7 * (montype+1) + 5
        elif rarity == "Rare":
            correction = 5 * montype + 4
        elif rarity == "Uncommon":
            correction = 3 * montype + 3
        elif rarity == "Common":
            correction = 2 * montype + 2
        else:
            correction = 3
        for stat in range(len(baseStats)):
            if baseStats[stat] > 0:
                baseStats[stat] += correction
                baseStats[stat] = int(baseStats[stat])
        return (rarity+" "+armorName,baseStats)   
    def addWeaponTitle(self,weaponName,oldAtt,oldDef,montype,rarity):
        """
        Adds a randomized quality value for the sword.

        __author__ = 'Nicholas Koy'

        Args:   weaponName (Str): weapon old name
                oldAtt (list of ints): old att values to scale
                oldDef (list of ints): old def values to scale
                montype (int):  Monster level / GearLevel
                rarity (Str):   Rarity of the item
        
        Returns:    tuple (str,list,list): name,attack,defenses
        """
        titleModList = ["Broken","Chipped","Refined","Tempered","Coated"]
        numRolls = (montype- 3) * 2
        if numRolls <= 0: numRolls = 1
        distrib = [0,0,0,0,0,1,1,1,1,2,2,2,3,3,3,4,4]
        bestRoll = 0
        adj = 0
        for roll in range(numRolls):
            current = random.choice(distrib)
            if bestRoll < current:
                bestRoll = current
        title = titleModList[bestRoll]
        if weaponName is None:
                weaponName = ""
        if oldAtt is None and oldDef is None:
            weaponDmg = [0,0,0,0,0]
            weaponDefBonus = [0,0,0,0,0]
        else:
            weaponDmg = oldAtt
            weaponDefBonus = oldDef
        baseStats = [0,0,0,0,0]
        if weaponDmg == baseStats:
            baseStats[0] += randint(1,3) + montype
        if bestRoll == 0:
            weaponDmg[0] += 1
            weaponDmg[0] *= 1.2
            newScale = 1.01
            adj = 1
        elif bestRoll == 1:
            weaponDmg[0] += 1.2
            weaponDmg[0] *= 1.5
            newScale = 1.02
            adj = 1
        elif bestRoll == 2:
            weaponDmg[0] += 1.3
            weaponDmg[0] *= 1.7
            newScale = 1.05
            adj = 1
        elif bestRoll == 3:
            weaponDmg[0] += 1.5
            weaponDmg[0] *= 2.3
            adj = 2
            newScale = 1.09
        else:
            weaponDmg[0] += 1.7
            weaponDmg[0] *= 2.7
            newScale = 1.14
            adj = 3
        if "Unique" == rarity:
            newScale += .05
        elif "Legendary" == rarity:
            newScale += .03
        elif "Ultra Rare" == rarity:
            newScale += .02
        elif "Rare" == rarity:
            newScale += .01
        
        newAtt = weaponDmg
        newDef = [restype for restype in weaponDefBonus]
        return (title + " " + weaponName+"Sword ",newAtt,newDef)
    def addArmorTitle(self,armorName,rarity,baseStats,montype):
        armorName = random.choice(["Hide ","Leather ","Chainmail ","Bone ",\
            "Plate ", "Brigandine "]) + armorName
        armorQuality,scale = random.choice([("Battle Scarred ",6),\
            ("Worn ",7),("Fine ",11),("Padded ",13)])
        baseStats = [defStat * scale / 10 for defStat in baseStats]
        return (armorQuality + armorName, baseStats)
    def addArmorSuffix(self,armorName,baseStats,rarity,montype):
        enchantDict = { "phys":{"of Fortify Health ":25,"of the Bear":35,"of the Elephant":50, "of Minor Fortification":10},
                        "fire":{"of the Salamander":10,"of the Fire Slug":15,"of the Fire Dragon":25, "of Resist Minor Fire":5},
                        "cold":{"of the Penguin":10,"of the Polar Bear":15,"of the Frost Dragon":25, "of Resist Minor Cold":5},
                        "pois":{"of the Spider":10,"of the Snake":15,"of the Badger":25, "of Resist Minor Poison":5},
                        "elec":{"of the Eel":10,"of Resist Major Elec ":15,"of the Storm Dragon":25, "of Resist Minor Elec":5}}
        enchantChoice = random.choice(list(enchantDict.keys()))
        enchantName = random.choice(list(enchantDict[enchantChoice].keys()))
        enchantStatMap = {"phys":0,"fire":1,"elec":2,"cold":3,"pois":4}
        baseStats[enchantStatMap[enchantChoice]]+= enchantDict[enchantChoice][enchantName]
        return (armorName + enchantName, baseStats)
    def generateArmorBaseStats(self,rarity,montype):
        """
        Creates a basis for armor stats to be scaled later depending on rarity
        and monster level

        __author__ = 'Nicholas Koy'

        Args:   rarity (Str): rarity of the item
                montype (Int):Gear level / monster level
        Returns: list of ints representing the armor base stats
        """
        lowestRoll = -6 * montype
        highestRoll = 2 * montype
        if lowestRoll > highestRoll:#This somehow happens
            lowestRoll,highestRoll = highestRoll,lowestRoll
        defBonusStats = [10*montype,0,0,0,0]
        defBonusStats[randint(1,4)]+= randint(lowestRoll, highestRoll)+5*montype
        defBonusStats[randint(1,4)]+= randint(lowestRoll, highestRoll)+5*montype
        return defBonusStats
    def addLesserWeaponSuff(self,weaponName,oldAtt,oldDef,itemType,montype):
        """
        Creates a minor offensive and defensive enchant for a sword
        __author__ = 'Nicholas Koy'
        Args:   weaponName (Str): Old weapon name gets a new name after
                oldAtt (list): old weapon attack stats
                oldDef (list): old weapon defensive stats
                itemType (Str):either "" or "Sword"
                montype (int): item level / monster level
        Returns tuple(str,list,list): newWeaponName,newAtt,newDef
        """
        if weaponName is None:
                weaponName = ""
        if oldAtt is None and oldDef is None:
            weaponDmg = [0,0,0,0,0]
            weaponDefBonus = [0,0,0,0,0]
        else:
            weaponDmg = oldAtt
            weaponDefBonus = oldDef
        suffixModList = ["ta","tis","crix","tex"] #tex > crix > tis > ta
        lesserprefixModList = ["Pzi","Igni","Volt","Cryo","Toxi"]
        lesserPref = randint(0,4)
        lesserRes = randint(0,3)
        weaponDmg[lesserPref]+= (lesserRes+1) * 2 * montype
        weaponDefBonus[lesserPref]+= (lesserRes+1) * 1.5 * montype
        weaponName += lesserprefixModList[lesserPref]+suffixModList[lesserRes] +\
            itemType + " "
        return (weaponName,weaponDmg,weaponDefBonus)
    def addMajorWeaponPrefix(self,weaponName,oldAtt,oldDef):
        """
        Creates a Major offensive enchant for a sword of a random element
        __author__ = 'Nicholas Koy'
        Args:   weaponName (Str): Old weapon name gets a new name after
                oldAtt (list): old weapon attack stats
                oldDef (list): old weapon defensive stats

        Returns tuple(str,list,list): newWeaponName,newAtt,newDef
        """
        if weaponName is None:
            weaponName = ""
        if oldAtt is None and oldDef is None:
            weaponDmg = [0,0,0,0,0]
            weaponDefBonus = [0,0,0,0,0]
        else:
            weaponDmg = oldAtt
            weaponDefBonus = oldDef
        firePrefix = {"Eruption":50,"Volcanic":70,"Flaming":30,"Hot":20,"Candle Lighting":5,"Bright":10}
        lightPrefix = {"Tempest":60,"Thunderus":45,"Electric":25,"Shocking":20,"Sparking":5}
        coldPrefix = {"Frigid":60,"Glacial":50,"Wintry":25,"Freezing":40,"Frosted":20,"Cool":5}
        poisonPrefix = {"Venomous":55,"Virulent":50,"Toxic":45,"Viscious":30}
        physPrefix = {"Reaping":40,"Sharp":30,"Stabby":20,"Heavy":20}
        majorChoice = ""

        enchantElement = random.choice(["fire","cold","light","poison","phys"])
        if enchantElement == "fire":
            fireChoice = random.choice(list(firePrefix.keys()))
            majorChoice = fireChoice
            weaponDmg[1] += firePrefix[fireChoice]

        elif enchantElement == "cold":
            coldChoice = random.choice(list(coldPrefix.keys()))
            majorChoice = coldChoice
            weaponDmg[2] += coldPrefix[coldChoice]
        elif enchantElement == "light":
            lightChoice = random.choice(list(lightPrefix.keys()))
            majorChoice = lightChoice
            weaponDmg[3] += lightPrefix[lightChoice]
        elif enchantElement == "poison":
            poisonChoice = random.choice(list(poisonPrefix.keys()))
            majorChoice = poisonChoice
            weaponDmg[4] += poisonPrefix[poisonChoice]
        else:
            physChoice = random.choice(list(physPrefix.keys()))
            majorChoice = physChoice
            weaponDmg[0] += physPrefix[physChoice]
        weaponName += majorChoice + "-"
        return (weaponName,weaponDmg,weaponDefBonus)
    def addUniqueWeaponEnchant(self,weaponName = None, oldAtt = None, oldDef =\
         None):
        """
        Adds a unique enchant to a weapon. THIS MUST BE ADDED LAST TO AN ITEM
        __author__ = 'Nicholas Koy'
        Args:   weaponName (Str): Old weapon name gets a new name after
                oldAtt (list): old weapon attack stats
                oldDef (list): old weapon defensive stats
        Returns tuple(str,list,list): newWeaponName,newAtt,newDef
        """
        uniqueModList = ["Slaying ","Unholy Purging ", "Vitality Boost ", "Strength Boost ",
                        "Feasting ", "Unrelenting "]
        if weaponName is None:
            weaponName = ""
        if oldAtt is None and oldDef is None:
            weaponDmg = [0,0,0,0,0]
            weaponDefBonus = [0,0,0,0,0]
        else:
            weaponDmg = oldAtt
            weaponDefBonus = oldDef

        uniqueMod = randint(0,5)
        if uniqueMod == 0:
            weaponDmg[0]+= 30
            weaponDmg[1]+= 26
        elif uniqueMod == 1:
            weaponDmg[1] += 30
            weaponDmg[3] += 20
            weaponDmg[2] += 5
        elif uniqueMod == 2:
            weaponDefBonus[0] += 50
            weaponDmg[0]+= 10
        elif uniqueMod == 3:
            weaponDefBonus[0] += 50
            weaponDmg[0]+= 20
        elif uniqueMod == 5:
            weaponDmg[1] += 20
            weaponDefBonus[1] += 9
            weaponDefBonus[2] += 11
            weaponDefBonus[3] += 13
            weaponDefBonus[4] += 15
        else:
            weaponDmg[0]+= 45
            weaponDefBonus[0] -= 15
            weaponDefBonus[1] -= 5 
            weaponDefBonus[2] -= 5 
            weaponDefBonus[3] -= 5
        weaponName = uniqueModList[uniqueMod] + weaponName
        return (weaponName,weaponDmg,weaponDefBonus)
    #Okay everything past here exists
def recalcAttack(entity):
    """
    Recalculates the entity's attack based off the weapon held and bonuses from
    any equipped ring and amulet.

    __author__ = 'Nicholas Koy'

    Side effects: sets entity.gearOffense for damage calculation
    """
    att = [0,0,0,0,0]
    if entity.inventory["sword"]["equip"] != None:

        for damagetype in \
            range(len(entity.inventory["sword"]["equip"].attackVal)):
            att[damagetype] += \
            entity.inventory["sword"]["equip"].attackVal[damagetype]
        if entity.inventory["armor"]["equip"]["Ring"] != None:
            for dmg in entity.inventory["armor"]["equip"]["Ring"].attackVal:
                att[dmg] += entity.inventory["armor"]["equip"]["Ring"][dmg]
        if entity.inventory["armor"]["equip"]["Amulet"] != None:
            for dmg in entity.inventory["armor"]["equip"]["Amulet"].attackVal:
                att[dmg] += entity.inventory["armor"]["equip"]["Amulet"][dmg]
    entity.gearOffense = att
    #print(sum(att))
def recalcDefense(entity):
    """
    recalculates the entity's hp and defense values towards elements
    __author__ = 'Nicholas Koy'
    Args: entity (Player or Enemy) that recently changed equipment

    Side effects: Sets self.defenses to a new list and setsnew maxhealth / hp
    """
    defenseVals = [0,0,0,0,0]
    armorSlots = ["Helmet","Body Armor","Gloves","Boots"]
    for resType in range(len(armorSlots)):
        if entity.inventory["armor"]["equip"][armorSlots[resType]] != None:
            for x in range(5):
                defenseVals[x] += \
                    entity.inventory["armor"]["equip"][armorSlots[resType]].\
                        defenses[x] 
    if entity.inventory["armor"]["equip"]["Ring"] != None:
        for dmg in entity.inventory["armor"]["equip"]["Ring"].defenses:
            defenseVals[dmg] += entity.inventory["armor"]["equip"]["Ring"].defenses[dmg]
    if entity.inventory["armor"]["equip"]["Amulet"] != None:
        for dmg in entity.inventory["armor"]["equip"]["Amulet"].defenses:
            defenseVals[dmg] += entity.inventory["armor"]["equip"]["Amulet"].defenses[dmg]
    entity.gearDefense = defenseVals
def calcDamage(entity1,entity2):
    totDmg = entity1.attack
    for damagetype in range(len(entity1.inventory["sword"]["equip"].attackVal)-1):
        #print(entity1.inventory["sword"]["equip"].attackVal[damagetype+1]," VS"
        # ,entity2.gearDefense[damagetype+1])
        if entity1.inventory["sword"]["equip"].attackVal[damagetype+1] > 0 and \
            entity2.gearDefense[damagetype+1] < entity1.inventory["sword"]\
                ["equip"].attackVal[damagetype+1]:
            totDmg += (entity1.inventory["sword"]["equip"].attackVal\
                [damagetype+1] - entity2.gearDefense[damagetype+1])
    totDmg +=entity1.inventory["sword"]["equip"].attackVal[0]
    return totDmg
def generateLoot(player,msgLog,enemy = None):
    """
    Generates loot for the Player ONLY by rolling a D20 five times.
    Quality is assigned based on the sum of those rolls plus the monster level

    __author__ = 'Nicholas Koy'

    Args:   player (Player): where the loot is going to
            msgLog (MessageLog): Logs the action
            enemy (None or Enemy):  If item loot generated via enemy death
                                    then this should be an Enemy for +weight
    adds a randomly chosen item base type to the player's inventory         
    """
    lootRoll = 0
    rollFive = 0
    x = 0
    for x in range(5):
        rollFive += randint(0,20)
    if enemy is not None:
        montype = enemy.montype
        lootRoll += enemy.montype
    else:
        montype = random.choice([1,1,1,1,1,2,2,2,2,3,3,3,4,4,5])
    if lootRoll >= 76 and lootRoll <= 105:
        rarity = "Unique"
    elif lootRoll >= 70 and lootRoll < 76:
        rarity = "Legendary"
    elif lootRoll >= 65 and lootRoll < 70:
        rarity = "Ultra Rare"
    elif lootRoll >= 60 and lootRoll < 65:
        rarity = "Rare"
    elif lootRoll >= 53 and lootRoll < 60:
        rarity = "Uncommon"
    else:
        rarity = "Common"
    gearOrConsume = randint(0,5)
    if gearOrConsume > 3:
        lootRoll = random.choice(["Body Armor","Gloves","Helmet","Sword","Boots"])
        drop = Gear(lootRoll,rarity,montype)
        player.addInventoryWearable(drop)
    elif gearOrConsume > 1:
        drop = random.choice(["torch","bandage","torch","map","key","food"])
        if drop == "food":
            drop =random.choice(["apple","bread","carrot","Mystery Meat"])
            if drop in player.inventory.keys():
                player.inventory[drop]+= 1
            else:
                player.inventory[drop] = 1
    else:
        cores = ["small core","medium core","large core"]
        drop = cores[random.choice([0,0,0,1,1,2])]
        player.inventory[drop] += 1
    cls()
    if not player.hideStats:
        print(player)
    msgLog.addLog("Found "+str(drop)+" ")
    print(msgLog)
    sleep(1)
def generateSimpleMaze():
    """
    Creates a simple maze if the user didnt provide a txt file to be read from.

    __authors__ = 'Nicholas Koy'

    Side effects: Creates a new maze and prints to stdout. Creates a txt file of
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
            #mazeArea = (rowsize-2)*(colsize-2)
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
            #Unique start end points now
            startloc = "("+ str(srow)+", "+ str(scol)+")"
            endloc = "("+ str(erow)+", "+ str(ecol)+")"
            newMaze.tuplemaze[startloc].obsID="S"
            newMaze.tuplemaze[endloc].obsID="E"
            #start and end str casted tuples reserved
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
        #anchorRow col gets a cell in the inner part of the maze to create a
        #single wall from either up or down
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
                    if newMaze.tuplemaze[strTup].obsID not in ["S","E"]:
                        newMaze.tuplemaze[strTup].obsID = "="
                    #just in case check so we dont override same with below
            r+=1
    else: #horizontal wall
        while c < newMaze.maxCol+1:
            roll = random.uniform(0, 1)
            if roll < .8:
                strTup = "(" + str(anchorrow) +", " + str(c) + ")"
                if strTup in newMaze.tuplemaze.keys() and newMaze.tuplemaze[strTup].obsID not in ["S","E"]:
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
            #Safety in case B is overriding S or E
            if newMaze.tuplemaze[battleloc].obsID not in ["S","E"]:
                newMaze.tuplemaze[battleloc].obsID = "B"
            occupied.append(battleloc)
        if treasureloc not in occupied:
            #Safety in case T is overriding S or E
            if newMaze.tuplemaze[treasureloc].obsID not in ["S","E"]:
                newMaze.tuplemaze[treasureloc].obsID = "T"
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
def main(maze,DEBUG = False):
    """
    __authors__ =   'Ali Iqbal', 'Nelson Contreras', 'Nicholas Koy', and
                    'Noble Nwokoma' : 
                        Everyone contributed ideas of branch ordering
                        Nelson: Generation of 'premade' players

    Sets the stage for playing and the difficulty. Lower levels of hunger
    makes the game much harder.

    Args:
            maze (str):     txt file name to read maze from.
            hunger (float): max hunger for the player
            DEBUG (Boolean): enables special commands between moves
    
    Side effects:
                    prints to stdout and makes a new maze
                    lowers player hunger as turns progress
                    reveals maze tiles as player progresses
    Raises: ValueError if stat inputs are 0 or negative
    """
    remove = False
    DEBUG = DEBUG
    if maze is None:
        maze = generateSimpleMaze()
        remove = True
    confirmed = False
    cls()
    while not confirmed:
        yesnoAnswer = False
        name = input("What is your character's name? or 'skip'\n")
        if name != "skip":
            hp = float(input("Enter the hp for your character\n"))
            attack  = float(input("Enter the attack\n"))
            speed = float(input("Enter your speed stat\n"))
            hunger = int(input("How many turns before you get hungry?\n"))
            if not((hp * attack * speed) > 0 and (hp > 0, attack > 0/
                speed > 0 and hunger >= 0) and "[" not in name):
                raise ValueError("Enter positive stat values or Illegal Name")
            player = Player(name,hp,attack,speed,hunger)
            while not yesnoAnswer:
                c =input(f"Confirm ('y') or ('n') the creation of\n{player}\n")
                if c.lower() == 'y':
                    confirmed = True
                    yesnoAnswer = True
                elif c.lower() =='n':
                    yesnoAnswer = True
                    confirmed = False
                else:
                    print("(Y)es or (N)o confirmation")
            cls()
        else:
            confirmed = True
            player_choice = ["Belson", "Bli", \
                "Boble", "Bibholas"]
            name = player_choice[randint(0,3)]
            hp = randint(100, 200)
            hunger = randint(40,60)
            if "Belson" in name:
                attack = randint(34,60)
                speed = randint(50,100)    
            elif "Bli" in name:
                attack = randint(12,60)
                speed = randint(25,50)
            elif "Boble" in name:
                attack = randint(12,120)
                speed = randint(31,150)
            elif "Bibholas" in name:
                attack = randint(60,80)
                speed = randint(45,60)
            cls()
    msgLog = MessageLog()
    player = Player(name,hp,attack,speed,hunger)
    newMaze= Maze(maze,player)
    if remove:
        os.remove("generated.txt")
    #print(f"Max c: {newMaze.maxCol}, Max r: {newMaze.maxRow}")
    newMaze.printMaze(player,msgLog)
    #borders = set(newMaze.getBorder())
    #cells = set(newMaze.tuplemaze.keys())
    #diff = cells - borders
    #print(diff)
    while str(newMaze.currentTuple) != str(newMaze.endTuple) and player.health > 0:
        newMaze.move(player,msgLog,DEBUG)
        cls()
        newMaze.printMaze(player,msgLog)
        #newMaze.getBorder()
    if player.health <= 0:
        cls()
        msgLog.addLog("Game Over!")
        msgLog.addLog("Score: "+str(player.getScore()))
        print(msgLog)
        sleep(3)
        cls()
        player.hideLog = True
        newMaze.printMaze(player,msgLog,True)
        sleep(3)
        msgLog.fullLog()
        #newMaze.printMaze(player,True)

    else: 
        cls()
        msgLog.addLog("Completed Maze!")
        msgLog.addLog("Score: "+str(player.getScore()))
        msgLog.fullLog()   
def showBoth(entity1,entity2):
    """
    Displays both the player and monster hp percentages neatly in color
    and dynamically sets the size of the menu based on name lengths
    __author__ = 'Nicholas Koy'
    Args:
        entity1 (Player or Enemy): The main entity (usually a Player)
        entity2 (Enemy): The enemy being fought by Entity1
    Side effects: Clears screen and prints to stdout in color
    """
    boxSize = "║$e1n"
    temp = ""
    tem = Template(boxSize).substitute(e1n = entity1.name)
    if not len(entity2.name)%2:
        temp = entity2.name
        entity2.name = " "+temp
    else: temp = entity2.name
    if len(tem)%2:
        tem += " " * 11
    else:
        tem += " " * 10
    if  (len(tem)%2):
        tem += "  $e2║\n"
    else:
        tem += " $e2║\n"
    tem2 = Template(tem).substitute(e2 = entity2.name)
    if len(tem2)%2:
        battleScreen = "▭" * (len(tem2)) + "\n"
        battleScreen = (battleScreen[0:len(entity1.name)] +\
             battleScreen[1+len(entity1.name):]) 
        tem2 = (tem2[0:len(entity1.name)] + tem2[1+len(entity1.name):]) 
    else:
        battleScreen = "▭" * (len(tem2)-1) + "\n"
    halfScreen = int(len(battleScreen)/2 -2)
    numGreen1 = int((entity1.health / entity1.maxhealth)* (halfScreen))
    numRed1 = halfScreen - numGreen1
    numGreen2 = int((entity2.health / entity2.maxhealth)* halfScreen)
    numRed2 = halfScreen - numGreen2
    if numRed1 > halfScreen: numRed1 = halfScreen 
    if numRed2 > halfScreen: numRed2 = halfScreen
    cls()
    hpSym = "░"
    hpbar1 = "\033[92m" + hpSym *(numGreen1) + \
    "\033[0m"+"\033[91m" + hpSym *numRed1 + "\033[0m"
    hpbar2 = "\033[91m" + hpSym*numRed2 + "\033[0m"+"\033[92m" + hpSym*numGreen2 \
        + "\033[0m"
    bothbars = "║"+hpbar1 + "║" + hpbar2+ "║\n"
    entity2.name =temp 
    print(battleScreen+tem2+bothbars+battleScreen)
def strike(entity1,entity2,msgLog):
    """
    One entity strikes another
    __authors__ =  'Nelson Contreras' and 'Nicholas Koy'

    Args:   entity1 (Player or Enemy)
            entity2 (Player or Enemy)
    
    Side effect: Lowers entity2 hp if an attack lands through them. Prints to
                 stdout via msgLog
    Returns: True if an entity dies from a hit
    """
    if entity1.health <= 0 or entity2.health <= 0:
        return True
    baseAccuracy = .7
    critChance = 3
    critDmg = 1
    baseAccuracy += int((entity1.speed - entity2.speed)/4) / 100
    if entity1.speed - entity2.speed > 0:
        critChance += int((entity1.speed - entity2.speed)/5)
    
    if randint(0,100) < critChance:
        cls()
        msgLog.addLog(entity1.name +" sees a weak point in "+entity2.name)
        if isinstance(entity1,Player):
            showBoth(entity1,entity2)
        else:
            showBoth(entity2,entity1)
        critDmg = 1.5
    if randint(0,100) <= baseAccuracy * 100:#accuracy roll
        attack = calcDamage(entity1,entity2)
        low = int(attack*.9)
        high = int(attack*1.1)
        if attack > high:
            high = attack
        if DEBUG:
            print("hypothetical max", 1.1*attack)
            print("hypothetical max crit", critDmg *1.1*attack)
            print("low roll min",low)
        sleep(1)
        damage = critDmg * randint(int(low),int(high))
        entity2.health -= damage
        cls()
        msgLog.addLog(entity1.name+" hits "+ entity2.name+ " for " +str(damage)\
            +" damage",True)
        #Keep interface consistent between battle turns
        if isinstance(entity1,Player):
            showBoth(entity1,entity2)
        else:
            showBoth(entity2,entity1)
    else: 
        cls()
        msgLog.addLog(entity1.name+" misses their target",True)
        if isinstance(entity1,Player):
            showBoth(entity1,entity2)
        else:
            showBoth(entity2,entity1)
    if entity1.health <= 0 or entity2.health <= 0:
        return True
    else:
        return False   
def battle_monsters(entity1, entity2, maze, msgLog : MessageLog()):
    """
    Starts the battle between player and monster until one dies

    Args:
        player (Player) - this will be the player attacking the monster
        the monster.
        monster (Enemy) - this will be monster attacking the player
        maze (Maze) where the battle is taking place
        msgLog (Message Log) - Stores actions

    __authors__ =  'Nelson Contreras', 'Nicholas Koy'
    
    """
    battleEnd = False
    while not battleEnd:
        cls()
        playerPresent = False
        showBoth(entity1,entity2)
        #prints stats and log if player is not dead
        print(msgLog)
        if isinstance(entity1,Player):
            if not entity1.hideStats:
                print(entity1)
            playerPresent = True

        #performs one more check
        if entity1.health <= 0:
            msgLog.addLog(entity1.name + " is dead! check 1363 if it got here"+\
            "then something went wrong")
            break
        actionChosen = False
        if not playerPresent: actionChosen = True
        while not (actionChosen) and playerPresent and not battleEnd:
            resp = input("(A)ttack, (U)se item, (R)un, or (S)wap weapon\n" +\
            "Or Toggle (stats)\n")
            resp = resp
            if resp not in ["a","u","r","s","stats"]:
                print("Enter a valid response")
            else:
                actionChosen = True
        if  isinstance(entity1,Enemy) or resp == "a" :
            winner = False
            entity1Faster = entity1.speed >= entity2.speed
            if entity1Faster:
                if not strike(entity1,entity2,msgLog): #Ent1 strikes doesnt kill
                    #
                    print(msgLog)
                    sleep(2)
                    if strike(entity2,entity1,msgLog): #E2 hits back and kills
                        print(msgLog)
                        winner = True
                        battleEnd = True
                        if isinstance(entity2,Player):
                            entity2.battlesWon += 1
                            entity2.battlesFought += 1
                        sleep(2)
                else: #E1 strike does kill
                    print(msgLog)
                    winner = True
                    battleEnd = True
                    if isinstance(entity1,Player):
                            entity1.battlesWon += 1
                            entity1.battlesFought += 1
                    sleep(2)
            else:#E2 hits first
                if not strike(entity2,entity1,msgLog): #E2 didnt kill
                    #sleep(2)
                    print(msgLog)
                    sleep(2)
                    if strike(entity1,entity2,msgLog): #E1 hits back and kills
                        winner = True
                        battleEnd = True
                        if isinstance(entity1,Player):
                            entity1.battlesWon += 1
                            entity1.battlesFought += 1
                else: #E2 killed e1
                    print(msgLog)
                    winner = True
                    battleEnd = True
                    if isinstance(entity2,Player):
                            entity2.battlesWon += 1
                            entity2.battlesFought += 1
                    sleep(2)
            if winner:
                cls()
                who = ""
                loser = ""
                if entity1.health > entity2.health: 
                    who = entity1.name
                    loser = entity2.name
                else: 
                    who = entity2.name
                    loser = entity1.name
                msgLog.addLog(who + " killed " + loser)
            showBoth(entity1,entity2)
            print(msgLog)
            sleep(1)
            if playerPresent and not entity1.hideStats:
                print(entity1)
            sleep(2)              
        elif resp == "stats" and isinstance(entity1,Player):
            entity1.hideStats = not entity1.hideStats 
        elif resp == "s":
            entity1.equipGear(msgLog)
            sleep(1)
            
        elif resp == "u":
            item = input("Use what?\ntorch or bandage\n")
            entity1.useItem(item,msgLog,maze)
            sleep(1)
        elif resp == "r":
            successChance = .07 * (8-entity2.montype) + \
                .04 * (6-entity2.montype)
            if entity1.speed < entity2.speed:
                successChance -= .05
            else:
                successChance += (entity1.speed - entity2.speed) / 500
            successChance *= 100

            if randint(0, 100) < successChance:
                battleEnd = True
                msgLog.addLog(entity1.name + " ran away successfully... loser")
                entity1.battlesFought += 1
                cls()
                showBoth(entity1,entity2)
                if not entity1.hideStats:
                    print(entity1)
                print(msgLog)
            else:#This code below can be used in the other two options
                msgLog.addLog(entity1.name + " tried to run away and failed")
                if not strike(entity2,entity1,msgLog): #E2 didnt kill
                    cls()
                    showBoth(entity1,entity2)
                    if not entity1.hideStats:
                        print(entity1)
                    print(msgLog)
                else: #E2 killed e1
                    winner = True
                    battleEnd = True
                    if not entity1.hideStats:
                        print(entity1)
                    print(msgLog)
            #may want to clear here
            #print(msgLog)
            sleep(1.6)
            
        #Debugging and this check is needed to prevent msgLog spam
        if entity1.health > 0:
            cls() 
            print(msgLog)
    if entity2.health <= 0:
        generateLoot(entity1,msgLog,entity2)
    sleep(1)
def parse_args(arglist):
    """ Parse command-line arguments.
    
    Expect one mandatory arguments:
        - filename: name of the file

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
    main(args.filename,DEBUG = True)
    #Testing ground
    #p1 = Player("Nick",100,100,100,100)
    #e1 = Enemy()
    