from pytest import approx, raises as pytest_raises
import dungeon_crawl as dg
import sys
import os
import builtins
from unittest import mock
from unittest.mock import patch
from time import sleep
def test_playerInit():
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
def test_useItem(capsys):
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