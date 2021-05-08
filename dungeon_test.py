from pytest import approx, raises as pytest_raises
import dungeon_crawl as dg
import sys
import os
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
    p = "test_maze.txt" 
    msglog = dg.MessageLog()
    name,hp,attack,speed,hunger = "Bob",1000,2000,3000,4000
    player = dg.Player(name,hp,attack,speed,hunger)
    testMaze = dg.Maze(p,player)
    testMaze.moveUp(player,msglog)
    testMaze.afterMove(player,msglog)
    print(player.inventory)
    assert "picked up" in str(msglog.log)
    testMaze.moveUp(player,msglog)
    testMaze.afterMove(player,msglog)
    assert "wall" in str(msglog.log)
    

