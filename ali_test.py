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
    score = gscore.getScore()
    player = dg.Player(name,hp,attack,speed,hunger)
    if i == "Diamond":
        score += player.inventory[i]*100
    elif(i == "Gold"):
        score += player.inventory[i]*80
    elif(i == "Emerald"):
        score += player.inventory[i]*60
    elif(i == "Silver"):
        score += player.inventory[i]*50
    elif(i == "Bronze"):
        score += player.inventory[i]*35
    elif(i == "Copper"):
        score += player.inventory[i]*20
    elif(i == "Amber"):
        score += player.inventory[i]*15
    elif(i == "Nugget"):
        score += player.inventory[i]*10
    elif i == "small core":
        score += (75 * player.inventory[i])
    elif i == "medium core":
        score += (125 * player.inventory[i])
    elif i == "large core":
        score += (200 * player.inventory[i])