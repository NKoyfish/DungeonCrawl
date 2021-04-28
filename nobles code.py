def revealMap(self,player):
        """
        This reveals the game map if it is in the players inventory
        Args:
            player(Player): The name of the payer in the game
            search through the players inventory to find the map.
        Side effects: Makes the map entire layout visible and reveals treasure
        """
        if player.inventory["map"] == 1:
            for cell in self.tuplemaze.keys():
                self.tuplemaze[cell].revealed = True
        
        
        print("Not yet implemented yet")

    def jumpWall(self, player):
        """
        this enables players who have the ability to jump over walls in the
        maze to be able to do so
        Args:
            player(String): The name of the player in the game
            it will evaluate the player and see if they have the ability to do
             so and if they can to execute, if not then the the code will break
        """
        row,col = self.currentTuple
        choose = False
        jumpable = ["c"]
        dirs = { "up":"("+str(row-1)+", "+str(col)+")","down":"("+str(row+1)+\
        ", "+str(col)+")","left":"("+str(row)+", "+str(col-1)+")",\
                 "right":"("+str(row)+", "+str(col+1)+")"}
        dirs2 = { "up":"("+str(row-2)+", "+str(col)+")","down":"("+str(row+2)+\
        ", "+str(col)+")","left":"("+str(row)+", "+str(col-2)+")",\
                 "right":"("+str(row)+", "+str(col+2)+")"}
        if player.abilityList["jump"] == 0:
            for jumpCheck in dirs: #check if a wall exists nearby
                if dirs[jumpCheck] in self.tuplemaze.keys():
                    if self.tuplemaze[dirs[jumpCheck]].obsID == "=" and \
                    (dirs2[jumpCheck] in self.tuplemaze.keys()) and \
                    self.tuplemaze[dirs2[jumpCheck]] != "=":
                        jumpable.append(jumpCheck)
            if len(jumpable) > 1:
                while not choose:
                    print(jumpable)
                    choice = input("which direction do you want to go to or enter c to quit\n")
                    if choice == "c":
                        break
                    elif choice in jumpable:
                        self.tuplemaze[str(self.currentTuple)].playerthere=False
                        newPos = dirs2[choice]
                        newPos2 = newPos
                        newPos = newPos.replace("(","")
                        newPos = newPos.replace(")","") 
                        newRow = int(newPos.split(", ") [0])
                        newCol = int(newPos.split(", ") [1])
                        self.tuplemaze[newPos2].playerthere=True 
                        self.tuplemaze[newPos2].revealed=True 
                        self.currentTuple = newRow, newCol
                        player.abilityList["jump"] = 5
                        choose = True
            else:
                print("their is no wall to jump")
        else:
            print("jump is still on cool down")
     