print("Hello") # Nick

print("INST-326 Final Project") #Nelson C.

"""
The project idea is to come up with a dungeon/maze game 
that pretty much consists of a text base system. Nicholas Koy
came up with the idea and we all agreed on the project and it typically 
runs by parsing a file. There will be barriers like walls and creatures 
along the text based maze. 

Further explanation (describe further):
methods (mentioning methods used): 
"""

class Greet():
    """Greets the user."""
    def __init__(self,language):
        self.language = language 
    
    #simple menu
    #2 methods don't do anything right now!
    def menuStartGame():
        print("---------Welcome to DungeonCrawl-----------")
        print()
        choice = input("""
                R: Reset Game
                S: Start Game
                Q: Quit Game

                Please Enter your Choice: """)
        
        if choice == "R" or choice == "r":
            login()
        elif choice == "S" or choice == "s":
            start()
        elif choice == "Q" or choice == "q":
            quit()
        else:
            print("Select either R or S")
            print("Please try again!")
            menuStartGame()

    def login():
        pass
    def start():
        pass

    

