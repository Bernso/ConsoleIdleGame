import math
import fileStuff
import boLogger
logger = boLogger.Logging()

class Game:
    def __init__(self):
        """
        What it does:
        - Creates 'data.json' if not already created
        - Gets time since last played
        - Calculate money generated since last played                   
        - Tells the user how long it has been since they last logged on
        - Greets the user
        - Opens the main menu
        """
        self.timeSinceLastStart = fileStuff.calcTime() 
        #print(self.timeSinceLastStart)
        fileStuff.moneyAFK(self.timeSinceLastStart)
        
        fileStuff.saveLastPlayed()
        self.timeSince = self.calcTimeSince(self.timeSinceLastStart)

        
        #logger.info(bold=True, text=f"It has been {self.timeSince["Minutes"]} mins since you have last played")
        print(f"Welcome to the Console Idle Game!\nIt has been {"new player" if self.timeSince["Seconds"] == 0 else self.timeSince["Seconds"]} seconds since you last played")
        self.mainMenu()
        
        
    def calcTimeSince(self, timeSince):
        return {
            "Days": int(timeSince/((60*60)*24)),
            "Hours": int(timeSince/(60*60)),
            "Minutes": int(timeSince/60),
            "Seconds": int(timeSince)
        }
    
    
        
    
    def mainMenu(self):
        options = {
            1: "My Rides",
            2: "All Rides",
            3: "Buy Rides",
            4: "View Money",
            5: "Update Money/Save",
            6: "Quit (saves aswell)"
        }
        while True:
            print(f"\nMain Menu")
            for key, value in options.items():
                print(f"{key} - {value}")
            
            try:
                choice = int(input("Select an option: "))
                if choice in options:
                    if choice == 1:
                        self.showUnlockedRides()                            # Update options
                    elif choice == 2:
                        self.showAllRides()
                    elif choice == 3:
                        self.buyRideMenu()
                    elif choice == 4:
                        self.viewMoney()
                    elif choice == 5: # Save and update money
                        self.save()
                    elif choice == 6:
                        self.save()
                        break
                else:
                    logger.warning("Please enter a valid option.")
            except ValueError as e:
                logger.warning("Value error")
                
        fileStuff.os.system('cls')         
        print("Bye")
    
    def showUnlockedRides(self):
        print("\nYour Rides:")
        rides = fileStuff.convertRidesListIntoProper()

        
        for key, value in rides.items():
            print(f"- {key}: level {value}")
    
    def showAllRides(self):
        rides = fileStuff.getAllRides()
        print("\nAll unlockable Rides are below:")
        print(rides)
    
    def viewMoney(self):
        print(f"\nYour balance: £{fileStuff.getMoney():,.2f}") # 2dp and "," serperator
    
    def updateMoney(self):
        fileStuff.moneyAFK(fileStuff.calcTime())
        fileStuff.saveLastPlayed()
        print("\nMoney Updated")
        
    def save(self):
        self.updateMoney()
        fileStuff.saveAll(fileStuff.getMoneyMethods())
    
    def buyRideMenu(self):
        print(f"\nNext Ride:")
        index = len(fileStuff.getMoneyMethods())
        price = fileStuff.getRideUnlockPrice(index)
        print(f" {fileStuff.RIDES[index]} - £{price}")
        
        
        choice = input("Would you like to buy this ride? (y/n) ")
        
        if choice.lower() == 'n':
            pass
        
        if fileStuff.getMoney() < price:
            print("\nSorry, you do not have enough money to buy this.")
        else:
            fileStuff.changeMoney('-', price)
            base = fileStuff.getMoneyMethods()
            base.append(1)
            
            fileStuff.saveMoneyMethods(base)
            print("Success!")
        
    
    # Add upgrade system, along with an organised menu, e.g. rides section of the menu for viewing all rides, buying and upgrading
        
        
if __name__ == '__main__':
    Game()
