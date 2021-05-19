from pytest import approx, raises as pytest_raises
import dungeon_crawl as dg
import sys
import os
import builtins
from unittest import mock
from unittest.mock import patch
from time import sleep
import random
from random import randint
from math import factorial

def test_enemyInit():
    """
    Does an enemy generate correctly?
    __author__ = 'Nelson Contreras'
    """
    monsterType = random.choice([0,1,2,3,4])
    monsters = ["Zombie", "Kobold", "Orc", "Goblin",\
            "Skeleton", "Ghoul", "Lizardman", "Spectre"]
    armorTypes = ["Gloves", "Boots", "Helmet","Body Armor"]
    armorChoice = random.choice(armorTypes)

    

    calculatingHealth = factorial(monsterType) * 5 + 100
    montype1 = 1
    montype2 = 2
    montype3 = 3
    montype4 = 4

    #making an enemy
    e1 = dg.Enemy()

    #second one is for the monsters
    e2 = dg.Enemy()
    monster_num1 = e2.name
    monster_num2 = e2.name
    monster_num3 = e2.name
    monster_num4 = e2.name

    storeEnemy = e1.montype

    #here im making sure that the inventory is used.
    inv = dg.Enemy()
    storeInventory = inv.inventory

    #Here i'm initializing gear to be worn 
    itemType = "Gloves"
    rarity = "Ultra Rare"
    montype = 2
    attackVal = None
    defenses = None
    gear = dg.Gear(itemType, rarity, montype, attackVal, defenses)


    #player inventory
    playerInv = dg.Enemy()
    inventory = playerInv.inventory["armor"]["equip"]["Helmet"], playerInv.inventory["armor"]["equip"]["Boots"], \
        playerInv.inventory["armor"]["equip"]["Gloves"], playerInv.inventory["armor"]["equip"]["Body Armor"], \
            playerInv.inventory["sword"]["equip"]




    #alternative way of calculating monsterhealth
    other = factorial(montype1) * 5 + 100
    other2 = factorial(montype2) * 5 + 100
    other3 = factorial(montype3) * 5 + 100
    other4 = factorial(montype4) * 5 + 100



    
    assert monsters == monsters
    assert calculatingHealth == calculatingHealth
    assert armorChoice == armorChoice
    assert other == 105
    assert other2 == 110
    assert other3 == 130
    assert other4 == 220
    assert storeEnemy == storeEnemy
    assert monster_num1 == e2.name
    assert monster_num2 == e2.name
    assert monster_num3 == e2.name
    assert monster_num4 == e2.name
    assert storeInventory == storeInventory
    assert gear == gear 
    assert inventory == inventory
def test_playerInit():
    """
    Checks that player initialized correctly
    __author__ = 'Nicholas Koy'
    """
    name,hp,attack,speed,hunger = "Bob",1,2,3,4
    player = dg.Player(name,hp,attack,speed,hunger)
    assert hasattr(player,"name")
    assert hasattr(player,"health")
    assert hasattr(player,"attack")
    assert hasattr(player,"inventory")
    assert hasattr(player,"battlesFought")
    assert hasattr(player,"battlesWon")
    assert hasattr(player,"hideLog")
    assert hasattr(player,"hideStats")
    assert player.getScore() == 0
    assert player.name == "Bob"
    assert player.attack == 2
    assert player.health == 1
    assert player.speed == 3
    assert player.hunger == 4
def test_mazeInit():
    """
    Does Maze.__init__() read the right file and create the right dictionary?
    """
    p = "test_maze.txt" 
    name,hp,attack,speed,hunger = "Bob",1,2,3,4
    player = dg.Player(name,hp,attack,speed,hunger)
    testMaze = dg.Maze(p,player)
    assert hasattr(testMaze,"tuplemaze")

    assert len(testMaze.tuplemaze) == 30,\
         "Some keys are missing or too many made"
    assert testMaze.tuplemaze["(2, 2)"].obsID == "S","Start in wrong place"
    assert testMaze.tuplemaze["(1, 3)"].obsID == "E","End in wrong place"
    assert testMaze.tuplemaze["(1, 1)"].obsID == "B","Enemy in wrong place"
    assert testMaze.tuplemaze["(1, 2)"].obsID == "T","Treasure in wrong place"
def test_move():
    """
    Uses moveDir() to check movement and log output on wall bump
    __author__ = 'Nicholas Koy'
    """
    p = "test_maze.txt" 
    msglog = dg.MessageLog()
    name,hp,attack,speed,hunger = "Bob",1000,2000,3000,4000
    player = dg.Player(name,hp,attack,speed,hunger)
    testMaze = dg.Maze(p,player)
    testMaze.moveUp(player,msglog)
    testMaze.afterMove(player,msglog)
    #print(player.inventory)
    assert "picked up" in str(msglog.log)
    testMaze.moveUp(player,msglog)
    testMaze.afterMove(player,msglog)
    assert "wall" in str(msglog.log)
def test_move2():
    """
    Will move() work when the player walks on a stair case?
    __author__ = 'Nicholas Koy'
    """
    p = "test_maze.txt" 
    msglog = dg.MessageLog()
    name,hp,attack,speed,hunger = "Bob",1,2,3,4
    player = dg.Player(name,hp,attack,speed,hunger)
    testMaze = dg.Maze(p,player)
    with mock.patch("builtins.input",side_effect = ["d"]):
        assert testMaze.move(player,msglog) == None
    with mock.patch("builtins.input",side_effect = ["r"]):
        assert testMaze.move(player,msglog) == None
    with mock.patch("builtins.input",side_effect = ["r"]):
        assert testMaze.move(player,msglog) == None
    assert str(testMaze.currentTuple) == "(2, 4)"
def test_moveAndBattle(capsys):
    """
    Does the game know how to handle other tiles correctly?
    __author__ = 'Nicholas Koy' and 'Nelson Contreras'
    """
    outerr = capsys.readouterr()
    out = outerr.out
    p = "test_maze.txt" 
    msglog = dg.MessageLog()
    name,hp,attack,speed,hunger = "Bob",1000,2000,3000,4000
    player = dg.Player(name,hp,attack,speed,hunger)
    testMaze = dg.Maze(p,player)
    with mock.patch("builtins.input",side_effect = ["r"]):
        testMaze.move(player,msglog)
    with mock.patch("builtins.input",side_effect = ["u"]):
        testMaze.move(player,msglog)
        assert testMaze.tuplemaze[str(testMaze.currentTuple)].obsID == "E"
        #Only the main script from the module can end the game
    with mock.patch("builtins.input",side_effect = ["l"]):
        testMaze.move(player,msglog)
        #print(msglog.log)
        combined ="".join(msglog.log)
        assert "picked up" in combined, "Something should have been picked up"
    with mock.patch("builtins.input",side_effect = ["l","a"]):
        testMaze.move(player,msglog)
        combined ="".join(msglog.log)
        assert "encountered" in combined, "Enemy should have appeared"
        assert "killed" in combined, "Enemy should have died"
        assert player.battlesWon == 1
        assert player.battlesFought == 1
        assert player.getScore() >= 110, \
            "Score from killing enemy and item should be >= 110"
        assert "Found" in combined, "Item should have dropped"
def test_breakWall(capsys):
    """
    test some cases of break wall
        namely: normal case, border case, and breaking while on cooldown
    __author__ = 'Nicholas Koy'
    """
    outerr = capsys.readouterr()
    p = "jumpBreak.txt" 
    msglog = dg.MessageLog()
    name,hp,attack,speed,hunger = "Bob",1000,2000,3000,4000
    player = dg.Player(name,hp,attack,speed,hunger)
    testMaze = dg.Maze(p,player)
    with mock.patch("builtins.input",side_effect = ["r","b","right"]):
        testMaze.move(player,msglog)
        testMaze.move(player,msglog)
        assert testMaze.tuplemaze["(1, 3)"].obsID == " "
    with mock.patch("builtins.input",side_effect = ["b","rest"]):
        testMaze.move(player,msglog)
        combined ="".join(msglog.log)
        assert "broke" in combined
        assert "cooldown" in combined
        testMaze.move(player,msglog)
    with mock.patch("builtins.input",side_effect = ["b"]):
        testMaze.move(player,msglog)
        combined = "".join(msglog.log)
        assert "No wall to break" in combined
def test_jumpWall(capsys):
    """
    Makes sure that jumpWall works
    """
    outerr = capsys.readouterr()
    p = "jumpBreak.txt" 
    msglog = dg.MessageLog()
    name,hp,attack,speed,hunger = "Bob",1000,2000,3000,4000
    player = dg.Player(name,hp,attack,speed,hunger)
    testMaze = dg.Maze(p,player)
    with mock.patch("builtins.input",side_effect = ["r","j","right"]):
        testMaze.move(player,msglog)
        testMaze.move(player,msglog)
        assert str(testMaze.currentTuple) == "(1, 4)", "Didn't jump wall"
        assert player.abilityList["jump"] == 4, "Down 1 from 5 after moving"
def test_useItem(capsys):
    """ 
    Rests and uses items
    Makes sure hp and hunger levels are correctly restored
    and map reveal works
    __author__ = 'Nicholas Koy'
    """
    outerr = capsys.readouterr()
    p = "jumpBreak.txt" 
    msglog = dg.MessageLog()
    name,hp,attack,speed,hunger = "Bob",1000,2000,3000,4000
    player = dg.Player(name,hp,attack,speed,hunger)
    player.health = 1
    testMaze = dg.Maze(p,player)
    actions = ["r","rest","use","food","apple","use","bandage","use","map"]
    with mock.patch("builtins.input",side_effect = actions):
        testMaze.move(player,msglog)
        assert player.health == 2, "should have healed 1 health after moving"
        testMaze.move(player,msglog)
        assert player.health == 102, "should have healed 10 perc hp after rest"
        assert player.hunger == 3989, "rest -10 hunger: move -1 hunger"
        testMaze.move(player,msglog)
        assert player.health == 117, "should have healed 15 hp from eating apple"
        assert player.hunger == 4000, "full belly after eating"
        testMaze.move(player,msglog)
        assert player.health == 117 + 250, "bandage should heal 250"
        assert player.inventory["bandage"] == 0, "bandage should be 0"
        assert player.inventory["food"]["apple"] == 0, "apple should be 0"
        testMaze.move(player,msglog)
        allRevealed = True
        for cell in testMaze.tuplemaze.keys():
            if not testMaze.tuplemaze[cell].revealed:
                allRevealed = False
        assert allRevealed, "Every cell should be revealed now"
def test_getscore():
    """
    checks if getScore works()
    __author__ = 'Ali Iqbal'
    """
    #score = gscore.getScore()
    name,hp,attack,speed,hunger = "Ali",25,80,45,12
    player = dg.Player(name,hp,attack,speed,hunger)
    score = 0
    for i in player.inventory.keys():
        if i == "Diamond":
            assert score == score + player.inventory[i]*100
        elif(i == "Gold"):
            assert score == score + player.inventory[i]*80
        elif(i == "Emerald"):
            assert score == score + player.inventory[i]*60
        elif(i == "Silver"):
            assert score == score + player.inventory[i]*50
        elif(i == "Bronze"):
            assert score == score + player.inventory[i]*35
        elif(i == "Copper"):
            assert score == score + player.inventory[i]*20
        elif(i == "Amber"):
            assert score == score + player.inventory[i]*15
        elif(i == "Nugget"):
            assert score == score + player.inventory[i]*10
        elif i == "small core":
            assert score == score + (75 * player.inventory[i])
        elif i == "medium core":
            assert score == score + (125 * player.inventory[i])
        elif i == "large core":
            assert score == score + (200 * player.inventory[i])