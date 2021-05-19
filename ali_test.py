#creating my test for getscore()
from pytest import approx, raises as pytest_raises
import dungeon_crawl as dg
import sys
import os
import builtins
from unittest import mock
from unittest.mock import patch
from time import sleep


def test_getscore():
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
            