from datetime import datetime
import json
import os
import math

JSON_FILE = 'data.json'
RIDES = [ # Ride name,  base price, base earnings
    ["Shooting Range",  2,          0],
    ["Haunted House",   5,          5000],
    ["Ferris Wheel",    10,         50000],
    ["Roller Coaster",  20,         500000],
    ["Drop Tower",      40,         6251250],
    ["Water Ski",       80,         78924590],
    ["Bumper Cars",     150,        95000000],
    ["Log Flume",       300,        120000000],
    ["Giant Swing",     600,        1800000000],
    ["Inverted Coaster",1200,       25000000000],
    ["Flying Theatre",  2500,       500000000000]
]



def getTime():
    """Returns the current datetime."""
    return datetime.now()

def readJson():
    """Reads the JSON file and returns the data, initializing it if not found."""
    if not os.path.exists(JSON_FILE):
        data = {
            "money_methods": [1], # Level 1 shooting range for new players
            "last_played": getTime().strftime("%Y-%m-%d %H:%M:%S"),
            "money": 0
        }
        writeJson(data)
        return data
    
    with open(JSON_FILE, 'r') as file:
        return json.load(file)

def writeJson(data):
    """Writes data to the JSON file."""
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def calcTime():
    """Calculates the time difference (in seconds) from the last recorded playtime."""
    data = readJson()
    now = getTime()
    past_time = datetime.strptime(data["last_played"], "%Y-%m-%d %H:%M:%S")
    return (now - past_time).total_seconds()

def saveLastPlayed():
    """Updates the last played time to the current time."""
    data = readJson()
    data["last_played"] = getTime().strftime("%Y-%m-%d %H:%M:%S")
    writeJson(data)

def saveMoneyMethods(methods: list):
    """Updates the money methods list in the JSON file."""
    data = readJson()
    data["money_methods"] = methods
    writeJson(data)

def getMoneyMethods():
    """Retrieves the money methods value from the JSON file."""
    return readJson()["money_methods"]

def saveAll(methods: list):
    """Saves both the last played time and money methods in a single operation."""
    data = {
        "last_played": getTime().strftime("%Y-%m-%d %H:%M:%S"),
        "money_methods": methods,
        "money": getMoney() # Just here so it doesn't accidentally get written out
    }
    writeJson(data)



def convertRidesListIntoProper():
    """Gets the original rides list of levels and makes it into a dictionary all pretty"""
    base = getMoneyMethods()
    
    return {RIDES[i][0]: base[i] for i in range(len(base))}

def getAllRides():
    """Displays all avalible rides to be unlocked"""
    ridesUnlocked = getMoneyMethods()
    string = ''
    index = 0
    for ride in RIDES:
        index += 1
        string += f"{index} - {ride[0]} {"(LOCKED)" if index > len(ridesUnlocked) else ''}{"\n" if index != len(RIDES) else ''}"
        
    return string

def getMoney():
    return readJson()['money']

def changeMoney(operator: str, amount):
    current = getMoney()
    
    if operator == '+':
        current += amount
    elif operator == '-':
        current -= amount
    elif operator == '/':
        current = current / amount
    elif operator == '*':
        current *= amount
    elif operator == '=':
        current = amount
        
    data = readJson()
    data['money'] = current
    writeJson(data)
    

def moneyAFK(timeSince):
    """
    Calculate money earned while away based on ride levels and time passed.
    Uses a logarithmic scaling to prevent exponential growth while still
    rewarding longer idle times.
    
    Args:
        timeSince: Number of seconds since last played
    """
    # Base earnings per minute (not per second to keep numbers manageable)
    
    
    levels = getMoneyMethods()
    current_money = getMoney()
    new_money = current_money
    minutes_passed = timeSince / 60  # Convert seconds to minutes
    
    # Calculate earnings for each unlocked ride
    for i in range(len(levels)):
        #ride_name = RIDES[i][0]
        level = levels[i]
        
        # Base earning calculation
        base_per_minute = RIDES[i][1]
        
        # Level multiplier (diminishing returns after level 10)
        level_multiplier = 1 + (level * 0.5 if level <= 10 else 5 + (level - 10) * 0.1)
        
        # Time multiplier (logarithmic scaling to prevent exponential growth)
        # log10(minutes + 1) provides a smooth curve that grows more slowly over time
        time_multiplier = 1 + math.log10(minutes_passed + 1) * 0.5
        
        # Calculate total earnings for this ride
        ride_earnings = base_per_minute * level_multiplier * time_multiplier * minutes_passed
        
        # Add to total
        new_money += ride_earnings
    
    # Round to 2 decimal places to prevent floating point errors
    new_money = round(new_money, 2)
    changeMoney('=', new_money)
    
    return new_money - current_money # The difference

def calcUpgradeCost(ride_index, current_level):
    """
    Calculate cost to upgrade a ride to the next level.
    Uses exponential scaling based on ride unlock cost.

    Args:
        ride_index: Index of the ride (0-4).
        current_level: Current level of the ride.

    Returns:
        Cost for next upgrade.
    """
    base_prices = getRideUnlockPrice()  # Get unlock prices for all rides
    ride_name = RIDES[ride_index][0]
    
    # Get unlock price of the ride, defaulting to 100 if not found
    unlock_price = base_prices.get(ride_name, 100)
    
    # Base cost is now scaled based on unlock price (divided to keep numbers reasonable)
    base_cost = max(100, unlock_price / 50)  # Minimum base cost is 100
    
    # Exponential cost scaling with ride-based multiplier
    return round(base_cost * (1.3 ** (current_level - 1)), 2)


def getRideUnlockPrice(ride_index=None):
    """
    Get the unlock price for a ride.
    
    Args:
        ride_index: Index of the ride (0-4). If None, returns dict of all prices.
    Returns:
        Price to unlock the ride, or dict of all ride prices
    """
    if ride_index is not None:
        return RIDES[ride_index][2]
    else:
        # Create a dictionary of ride names and their unlock prices
        return {ride[0]: ride[2] for ride in RIDES}

def upgradeRide(ride_index, times=1):
    data = readJson()
    levels = data["money_methods"]  # Ride levels list
    money = data["money"]

    if ride_index >= len(levels):
        print("You haven't unlocked this ride yet!")
        return False

    total_cost = 0
    current_level = levels[ride_index]
    
    # Calculate total cost first
    for i in range(times):
        upgrade_cost = calcUpgradeCost(ride_index, current_level + i)
        total_cost += upgrade_cost

    # Check if player can afford the total upgrade cost
    if money < total_cost:
        print(f"Not enough money to upgrade {RIDES[ride_index][0]}!")
        return False

    # If they can afford it, perform the upgrades
    money -= total_cost
    levels[ride_index] += times

    # Save the updated data
    data["money_methods"] = levels
    data["money"] = round(money, 2)
    writeJson(data)

    print(f"Upgraded {RIDES[ride_index][0]} to level {levels[ride_index]}")
    return True


def clear():
    os.system('cls')