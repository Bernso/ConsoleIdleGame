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
        fileStuff.clear()   
        self.timeSinceLastStart = fileStuff.calcTime() 
        gained = fileStuff.moneyAFK(self.timeSinceLastStart) # gained is the amount of money earned offline
        
        fileStuff.saveLastPlayed()                 
        self.timeSince = self.calcTimeSince(self.timeSinceLastStart)

        print(f"Welcome to the Console Idle Game!\nMoney gained: £{gained:,.2f}\n\nTime since last played:\n"
              f"- {self.timeSince["Seconds"]} seconds\n- {self.timeSince['Minutes']} minutes\n- {self.timeSince['Hours']} hours\n- {self.timeSince['Days']} days\n"
              )
        self.mainMenu()
        
        
    def calcTimeSince(self, timeSince):
        return {
            "Days": int(timeSince / ((60 * 60) * 24)),
            "Hours": int((timeSince / (60 * 60)) % 24),
            "Minutes": int((timeSince / 60) % 60),
            "Seconds": int(timeSince % 60),
            "Full": int(timeSince)
        }
    
    
        
    
    def mainMenu(self):
        options = {
            1: "Ride Menu",
            2: "View Money",
            3: "Update Money/Save",
            4: "Quit (Saves as well)"
        }
        while True:
            print(f"\nMain Menu")
            for key, value in options.items():
                print(f"{key} - {value}")
            
            try:
                choice = int(input("Select an option: "))
                if choice in options:
                    if choice == 1:
                        self.rideMenu()                            # Update options
                    elif choice == 2:
                        self.viewMoney()
                    elif choice == 3: # Save and update money
                        self.save()
                    elif choice == 4:
                        self.save()
                        break
                else:
                    fileStuff.clear()
                    logger.warning("Please enter a valid option.")
            except ValueError as e:
                fileStuff.clear()
                logger.warning("Value error")
                
        fileStuff.clear()        
        print("Bye")
    
    def rideMenu(self):
        fileStuff.clear()   
        options = {
            1: "Show unlocked rides",
            2: "Show all rides",
            3: "Buy a new ride",
            4: "Upgrade menu",
            5: "Go back to main menu"
        }
        while True:
            print("\nRide Menu")
            for key, value in options.items():
                print(f"{key} - {value}")
            
            try:
                choice = int(input("Select an option: "))
                if choice in options:
                    if choice == 1:
                        self.showUnlockedRides()
                    elif choice == 2:
                        self.showAllRides()
                    elif choice == 3:
                        self.buyRideMenu()
                    elif choice == 4:
                        self.upgradeMenu()
                    elif choice == 5:
                        fileStuff.clear()   
                        break
                else:
                    fileStuff.clear()
                    logger.warning("Please enter a valid option.")
            except ValueError as e:
                fileStuff.clear()
                logger.warning("Value error")
                
                        
    
    def upgradeMenu(self):
        fileStuff.clear()   
        options = {
            1: "Upgrade ride",
            2: "Return to Ride Menu"
        }
        
        while True:
            print("\nUpgrade Menu")
            for key, value in options.items():
                print(f"{key} - {value}")
            
            try:
                choice = int(input("Select an option: "))
                if choice in options:
                    if choice == 1:
                        self.upgradeRide()

                    elif choice == 2:
                        fileStuff.clear()
                        break
                else:
                    fileStuff.clear()
                    logger.warning("Please enter a valid option.")
            except ValueError as e:
                fileStuff.clear()
                logger.warning("Value error")
            
            
    def upgradeRide(self):
        fileStuff.clear()   
        self.showUnlockedRides()  # Print out all unlocked rides
        try:
            rideIndex = int(input("\nEnter the number related to the ride you want to upgrade: ")) - 1
            numTimes = int(input("\nHow many times would you like to upgrade? "))

            data = fileStuff.readJson()
            levels = data["money_methods"]

            if rideIndex < 0 or rideIndex >= len(levels):
                print("Invalid ride number. Please select a valid option.")
                return

            current_level = levels[rideIndex]

            total = 0
            for i in range(numTimes):
                temp = fileStuff.calcUpgradeCost(rideIndex, current_level + i)
                total += temp
            print(f"You have £{fileStuff.getMoney():,.2f}")
            choice = input(f"This upgrade will cost you £{total:,.2f}\nAre you sure you want to do this? (y/n) ")
            fileStuff.clear()
            if choice.lower() == 'y':
                fileStuff.upgradeRide(rideIndex, numTimes)  # No need to subtract 1 again
                print("Upgrade complete")
            else:
                print("Upgrade cancelled")
        except ValueError:
            fileStuff.clear()
            logger.warning("Invalid input. Please enter a number.")

            
    def showUnlockedRides(self):
        fileStuff.clear()   
        print("\nYour Rides:")
        rides = fileStuff.convertRidesListIntoProper()

        index = 1
        for key, value in rides.items():
            print(f"{index} - {key} (lv. {value})")
            index += 1
    
    def showAllRides(self):
        fileStuff.clear()   
        rides = fileStuff.getAllRides()
        print("\nAll unlockable Rides are below:")
        print(rides)
    
    def viewMoney(self):
        fileStuff.clear()   
        print(f"\nYour balance: £{fileStuff.getMoney():,.2f}") # 2dp and "," serperator
    
    def updateMoney(self):
        fileStuff.clear()   
        fileStuff.moneyAFK(fileStuff.calcTime())
        fileStuff.saveLastPlayed()
        print("\nMoney Updated")
        
    def save(self):
        self.updateMoney()
        fileStuff.saveAll(fileStuff.getMoneyMethods())
        print("\nSaved!")
    
    def buyRideMenu(self):
        fileStuff.clear()   
        print(f"\nNext Ride:")
        index = len(fileStuff.getMoneyMethods())
        price = fileStuff.getRideUnlockPrice(index)
        print(f" {fileStuff.RIDES[index][0]} - £{price:,.2f}")
        
        print(f"\nYou have £{fileStuff.getMoney():,.2f}")
        choice = input("Would you like to buy this ride? (y/n) ")
        
        if choice.lower() == 'y':
            
        
            if fileStuff.getMoney() < price:
                print("\nSorry, you do not have enough money to buy this.")
            else:
                fileStuff.changeMoney('-', price)
                base = fileStuff.getMoneyMethods()
                base.append(1)
                
                fileStuff.saveMoneyMethods(base)
                print("Success!")
        
    
    # Add an organised menu, e.g. rides section of the menu for viewing all rides, buying and upgrading
        
        
if __name__ == '__main__':
    Game()
