from pytest import approx, raises as pytest_raises
import dungeon_crawl as dg
import random
from random import randint
from math import factorial


#enemy _init_
#typeofMonster = monsterType.choice[randint(0,7)]
    #enemyType = dg.Enemy(typeofMonster)
    #print(typeofMonster)
    #enemyType = dg.Enemy(typeofMonster)
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

