from argparse import ArgumentParser
import sys
import curses
from time import sleep
import tempfile
import os
from math import factorial
import random
from random import randint
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
        self.inventory = {"map": 0, "sword": {"equip": attack, "unequip": [] },
        "armor" : {"equip": ("tunic", 0, 0, 5), "unequip": []}, "small core": 0, "medium core":0
        , "large core": 0}
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
        montype = random.choice([1,1,1,1,1,1,1,1,1,2,2,2,3,3,3,4,4,5])
        
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
        #balance
        self.attack /= 2 
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
    def __repr__(self):
        return self.name
def strike(entity1,entity2):
    """TENTATIVE VERSION
    Entity1 attacks entity2 and calcualtes remaining hp

    Args:   entity1 (Player or Enemy)
            entity2 (Player or Enemy)
    
    Side effect: Lowers entity2 hp if an attack lands through them
    """
    baseAccuracy = .7
    critChance = 3
    critDmg = 1
    baseAccuracy += int((entity1.speed - entity2.speed)/4) / 100
    if entity1.speed - entity2.speed > 0:
        critChance += int((entity1.speed - entity2.speed)/5)
    
    if randint(0,100) < critChance:
        print(f"{entity1} sees a weak point in {entity2}")
        critDmg = 1.5
    if randint(0,100) <= baseAccuracy * 100:#accuracy roll
        low = int(entity1.attack*.9)
        high = int(entity1.attack*1.1)
        damage = critDmg * randint(low,high)
        entity2.health -= damage
        print(f"{entity1} hit {entity2} for {damage} damage")
    else: print(f"{entity1.name} missed")
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
        playerFaster = player.speed >= monster.speed
        if playerFaster:
            if player.health <= 0 and monster.health > player.health:
                print(f"{monster.name} has won the battle against {player.name}!")
                battleEnd = True
            elif(monster.health <= 0 and player.health > monster.health):
                print(f"{player.name} won and {monster.name} has been defeated!")
                battleEnd = True
            elif(player.health <= 0 and monster.health <= 0):
                print(f"{player.name} and {monster.name} have slain each other!")
                battleEnd = True
            if not battleEnd:
                strike(player,monster)
                sleep(.2)
            if player.health <= 0 and monster.health > player.health:
                print(f"{monster.name} has won the battle against {player.name}!")
                battleEnd = True
            elif(monster.health <= 0 and player.health > monster.health):
                print(f"{player.name} won and {monster.name} has been defeated!")
                battleEnd = True
            elif(player.health <= 0 and monster.health <= 0):
                print(f"{player.name} and {monster.name} have slain each other!")
                battleEnd = True
            if not battleEnd:
                strike(monster,player)
                sleep(.2)
        else:
            if player.health <= 0 and monster.health > player.health:
                print(f"{monster.name} has won the battle against {player.name}!")
                if isinstance(player,Player):
                    player.battlesWon += 1
                    player.battlesFought += 1
                battleEnd = True
            elif(monster.health <= 0 and player.health \
                > monster.health):
                print(f"{player.name} won and {monster.name} has been defeated!")
                if isinstance(player,Player):
                    player.battlesWon += 1
                    player.battlesFought += 1
                battleEnd = True
            elif(player.health <= 0 and monster.health <= 0):#should never get here
                print(f"{player.name} and {monster.name} have slain each other!")
                battleEnd = True
            if not battleEnd:
                strike(monster,player)
                sleep(.2)
            if player.health <= 0 and monster.health > player.health:
                print(f"{monster.name} has won the battle against {player.name}!")
                battleEnd = True
            elif(monster.health <= 0 and player.health \
            > monster.health):
                print(f"{player.name} won and {monster.name} has been defeated!")
                if isinstance(player,Player):
                    player.battlesWon += 1
                    player.battlesFought += 1
                battleEnd = True
            elif(player.health <= 0 and monster.health <= 0):
                print(f"{player.name} and {monster.name} have slain each other!")
                battleEnd = True
            if not battleEnd:
                strike(player,monster)
                sleep(.2)

enemy1 = Enemy()   
enemy2 = Enemy()
player = Player("Nick",200,50,40)
print(f"{enemy1} has {enemy1.health}, {enemy2} has {enemy2.health}")
battle_monsters(player,enemy2)
print(f"{enemy1} has {enemy1.health}, {enemy2} has {enemy2.health}")
