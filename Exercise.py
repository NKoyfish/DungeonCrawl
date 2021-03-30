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
    
    #simple menu being created
    def menuStartGame():
        # still have to work on the reset and start button
        def reset():
            print("we still have to come up with a reset option")
        def start():
            print("have to make a start button option")
        

        print("---------Welcome to DungeonCrawl-----------")
        print()

        loop = True
        while loop:   
            choice = input("""
                R: Reset Game
                S: Start Game
                Q: Quit Game

                Please Enter your Choice: """)
            
            """
            this is only temporary, the break might not work when
            executing the reset button or the start button.
            for the time being its okay. 
            """
            if choice== "R" or choice == "r":     
                reset()
                break
            elif choice== "S" or choice == "s":
                start()
                break
            elif choice=="Q" or choice == "q":
                quit()
                loop=False 
            else:
                wrongChoice = input("Wrong option selection. Enter any key to try again: ") 

    menuStartGame()

    

