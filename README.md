# DungeonCrawl
INST326 Project
## How to run
run by entering 
### "python3 dungeon_crawl.py -filename maze3.txt"
or 
### "python dungeon_crawl.py -filename maze3.txt"
the -filename arg is optional and a maze will be generated for the user if a file is not provided
## Features to potentially add

## Features added as of 5/15/21
  - Enemies can move by enabling them. Enemies farther than 1.42 tiles randomly move to an open space
    enemies one tile away will attack the player
## Features and fixes as of 5/04/21
  - Added colors to the printMaze(), armor, weapons, and stat screen. Combat screen may be next
  - Changed the combat system from just taking an entity's strength and rolling from 90 to 110 %
    of that value. New combat calculates damage at a minimum of your base attack and any weaknesses
    to elements an enemy may have so long as you deal damage of that type.
  - Every Enemy spawns with at least one item but drops a different item on death.
  - main now has a DEBUG argument defaulted to False.
      DEBUG mode enables the user to auto create a set of armor and a weapon
      "armor" and "combatplus"
## Features and fixes as of 4/30/21
  - obscures tiles the player hasnt visited or been in one-cell proximity to
  - Neatly clears out prints (Before it would keep appending to the terminal with new maze prints)
  - generates random monsters and treasure for the player to encounter
  - player abilities : Jump and breakWall
  - can teleport using stair tiles
  - calculates score based off treasure obtained and battles won upon player death or completion 
  - players can rest to regain hp
  - upon player death or completion prints the whole adventure log
  - upon player death reveal the maze layout
  - player customization or auto generation if skipped
  - fixed the confusion between __str__() and __repr__()
  - auto-run fights between player and enemies

##  TODO:
  - Determine how we want stats to be printed.
  - Balance damage (low priority)
  - Make sure screens are consistent across new actions and clear screens
