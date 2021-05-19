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