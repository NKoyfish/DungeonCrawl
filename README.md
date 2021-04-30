# DungeonCrawl
INST326 Project
## How to run
run by entering 
### "python3 dungeon_crawl.py -filename maze3.txt"
or 
### "python dungeon_crawl.py -filename maze3.txt"
the -filename arg is optional and a maze will be generated for the user if a file is not provided

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

## TODO:
  - Neatly print HP bars of the Player and Enemy during battle below the Message Log
  - useItem() / eatFood()
  - Make enemies drop items and equipment depending on their level
  - allow the player to swap gear during exploration or in combat
  - allow the player to flee from combat
