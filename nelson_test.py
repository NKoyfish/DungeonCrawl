from pytest import approx, raises as pytest_raises
import dungeon_crawl as dg
import random
from random import randint
from math import factorial


def test_enemyInit():
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




