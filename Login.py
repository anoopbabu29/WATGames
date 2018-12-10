from Multiplayer.Multiplayer import Database, MultiplayerConnection
from Character import Character
from Character import Board
from Character import _Getch
from lootbox import Lootbox
from uuid import getnode as get_mac
import os
import random

#Colors
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[36m"
end = "\033[0m"

GREY    = '\33[90m'
CRED2    = '\33[91m'
CGREEN2  = '\33[92m'
CYELLOW2 = '\33[93m'
CBLUE2   = '\33[94m'
CVIOLET2 = '\33[95m'
CBEIGE2  = '\33[96m'
CWHITE2  = '\33[97m'

LB = Lootbox()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class LoginConnection():
    def __init__(self):
        self.db = Database()
        
    def login(self,username,password):
        links = self.db.get("Profiles")
        for key, value in links.items():
            if(key == username):
                if(value["password"] == password):
                    return self.dict2Character(value["Character"])
        return -1

    def create(self,username,password,character):
        links = self.db.get("Profiles")
        for key, value in links.items():
            if(key == username):
                return -1
            if(value != "base"):
                if(value["Address"] == str(get_mac())):
                    print("Error 666: Computer is trying to create multiple accounts")
                    return -1
        self.db.push("Profiles/" + username, character.getDict())
        self.db.push("Profiles/" + username, {"Character": character.getDict(), "password": password, "Address":str(get_mac())})
        return 1

    def dict2Character(self,d):
        name = d["Name"]
        style = d["Style"]
        weapon = d["Weapon"]["Name"]
        weaponbonus = (d["Weapon"]["Health"],d["Weapon"]["Attack"],d["Weapon"]["Defense"],d["Weapon"]["Speed"],d["Weapon"]["Type"])
        maxhealth = d["MaxHealth"]
        health = d["Health"]
        attack = d["Attack"]
        defense = d["Defense"]
        speed = d["Speed"]
        money = d["Money"]
        stash = d["Stash"]
        character = Character(Name=name, Style=style, Weapon=weapon, WeaponBonus=weaponbonus, Health=health, Attack=attack, Defense=defense, Speed=speed, Money=money,Stash=stash)
        character.MaxHealth = maxhealth

        return character

def begin(conn):
    conn = LoginConnection()
    character = -1

    comand = input("Login or Signup (l/s): ")
    while(comand != "l" and comand != "s"):
        comand = input("Login or Signin (l/s): ")

    if(comand == "l"):
        username = input("Username: ")
        password = input("Password: ")
        character = conn.login(username,password)
        while(character == -1):
            print("Incorrect Username or Password")
            username = input("Username: ")
            password = input("Password: ")
            character = conn.login(username,password)
    elif(comand == "s"):
        username = input("Username: ")
        password = input("Password: ")
        rpassword = input("Retype Password: ")
        while(password != rpassword):
            print("Passwords didn't match")
            password = input("Password: ")
            rpassword = input("Retype Password: ")

        gm = Character("Dummy","M")
        character = conn.create(username,password,gm)
        try:
            while(character == -1):
                print("Username " + username + " is already take")
                username = input("Username: ")
                character = conn.create(username,password,gm)

            #Character creation stuff here
            clear()
            types = {'S':'Swordsman','X':'Axeman','L':'Lancer','M':'Mage','A':'Archer'}
            Good = "no"
            while(Good != "y"):
                print("This is your Character Creation step")
                Name = input("Character Name: ")
                print("Your Charcter gets 2 battle styles")
                print("Type S for Swordsman, X for Axeman, L for Lancer, M for Mage, and A for Archer")
                Style1 = input("Character Style1: ").upper()
                Style2 = input("Character Style2: ").upper()
                while(not (Style1 in {'S','X','L','M','A'}) or not (Style1 in {'S','X','L','M','A'})):
                    print("Invalid Types: Type S for Swordsman, X for Axeman, L for Lancer, M for Mage, and A for Archer")
                    Style1 = input("Character Style1: ").upper()
                    Style2 = input("Character Style2: ").upper()

                clear()
                print("You are " + Name + " the " + types[Style1] + " and " + types[Style2])
                Good = input("Is this good (y/n)? ")
                
            clear()
            loot = LB.generate(Style1 + Style2)
            print("You Got:",loot)
            print()
            input("type anything to coninue... ")
            Weapon = loot[0]
            WeaponBonus = (loot[1][0],loot[1][1],loot[1][2],loot[1][3],loot[1][4])

            #
            pool = 35
            Health = 40
            Attack = 40
            Defense = 20
            Speed = 5

            clear()
            while(pool != 0):
                print("Enter a stat and a valid number points to increase or decease it by until all points are used")
                print("Total Points Left:\n\n" + "\t" + str(pool) + "\n")
                print("[" + Style1 + ", " + Style2 + "] " + Name + "\t| Health: " + str(Health) + " Attack: " + str(Attack) + " Speed: " + str(Speed) + " Defense: " + str(Defense))
                print()
                stat = input("Stat: ").upper()
                while(not (stat in {'H','A','D','S'})):
                    print("Invalid stat enter (h, a, d, s) for (Health, Attack, Defense, Speed) respectively")
                    stat = input("Stat: ").upper()

                value = int(input("Points: "))
                while(value > pool):
                    print("Invalid point amount you have " + str(pool) + " points left")
                    value = int(input("Points: "))

                clear()
                if(stat == 'H'):
                    if(value + Health <= 60 and value + Health >= 40):
                        Health = Health + value
                        pool = pool - value
                    elif(value + Health > 60):
                        pool = pool - (60 - Health)
                        Health = 60
                        print("You Maxed Out Health\n")
                    elif(value + Health < 40):
                        pool = pool - (40 - Health)
                        Health = 40
                        print("Health is back at base stat\n")

                if(stat == 'A'):
                    if(value + Attack <= 60 and value + Attack >= 40):
                        Attack = Attack + value
                        pool = pool - value
                    elif(value + Attack > 60):
                        pool = pool - (60 - Attack)
                        Attack = 60
                        print("You Maxed Out Attack\n")
                    elif(value + Attack < 40):
                        pool = pool - (40 - Attack)
                        Attack = 40
                        print("Attack is back at base stat\n")

                if(stat == 'D'):
                    if(value + Defense <= 40 and value + Defense >= 20):
                        Defense = Defense + value
                        pool = pool - value
                    elif(value + Defense > 40):
                        pool = pool - (40 - Defense)
                        Defense = 40
                        print("You Maxed Out Defense\n")
                    elif(value + Defense < 20):
                        pool = pool - (20 - Defense)
                        Defense = 20
                        print("Defense is back at base stat\n")

                if(stat == 'S'):
                    if(value + Speed <= 25 and value + Speed >= 5):
                        Speed = Speed + value
                        pool = pool - value
                    elif(value + Speed > 25):
                        pool = pool - (25 - Speed)
                        Speed = 25
                        print("You Maxed Out Speed\n")
                    elif(value + Speed < 5):
                        pool = pool - (5 - Speed)
                        Speed = 5
                        print("Speed is back at base stat\n")
        except Exception as e:
            print(e)
            print("Signup was unsucessful")
            conn.db.delete("Profiles/" + username)
            return -1


        character = Character(Name=Name, Style=Style1 + Style2, Weapon=Weapon, WeaponBonus=WeaponBonus, Health=Health, Attack=Attack, Defense=Defense, Speed=Speed, Money=1005)

        #

        conn.db.push("Profiles/" + username + "/Character", character.getDict())

        character = conn.login(username,password)

    clear()
    character.show()
    print()
    return [character, username]

def getTrade(item,message):
    connection = MultiplayerConnection()
    clear()
    print()
    print("Trade Connection Setup For:",item)
    print()
    roomName = input("Enter Room Name: ")
    playerName = "Trader"
    roomSize = 2
    
    results = connection.start(roomName,playerName,roomSize,game={"Trader":item,"Proposed":"..."})
    while(results == -1):
        roomName = input("Enter Room Name Again: ")
        results = connection.start(roomName,playerName,roomSize)

    data = message
    try:
        connection.waitTurn(roomName,1)
        clear()
        print("Room " + roomName)
        print()
        print("Trading: ")
        print()
        trade = connection.getGame(roomName)
        print("You proposed:",trade["Trader"])
        print()
        print("They proposed:",trade["Proposed"])
        print()
        data = input("Do you accept this trade? (y/n) (or type q to quit): ")
        while(data.upper() != "Q" and data.upper() != "Y" and data.upper() != "N"):
            data = input("Invalid command. Do you accept this trade? (y/n) (or type q to quit): ")
        if(data.upper() == 'Y'):
            connection.passTurn(roomName,2)
            return trade["Proposed"]
        elif(data.upper() == 'N' or data.upper() == 'Q'):
            trade["Trader"] = {"Name":"Empty","WeaponBouns":{"Health":0,"Attack":0,"Defense":0,"Speed":0}}
        connection.pushGame(roomName,trade)
        connection.passTurn(roomName,2)
    except KeyboardInterrupt:
        connection.close(roomName)
        return -1
    return -1

def joinTrade(item):
    connection = MultiplayerConnection()
    clear()
    print()
    print("Trade Connection Setup For:",item)
    print()
    roomName = input("Enter Room Name: ")
    playerName = "Proposer"

    results = connection.join(roomName,playerName)
    while(results < 0):
        if(results == -1):
            roomName = input("Enter Room Name Again: ")
        elif(results == -2):
            playerName = input("Enter Player Name Again: ")
        results = connection.join(roomName,playerName)

    positon = results
    roomSize = connection.getRoomSize(roomName)
    connection.passTurn(roomName,(positon % roomSize) + 1)
    trade = connection.getGame(roomName)
    print(trade)
    trade["Proposed"] = item
    connection.pushGame(roomName,trade)
    data = "start"
    counter = 0
    try:  
        while(data.upper() != "Q" and data.upper() != "N"):
            connection.waitTurn(roomName,positon)
            clear()
            print("Room " + roomName)
            print()
            trade = connection.getGame(roomName)
            print("You proposed:",trade["Proposed"])
            print()
            print("They proposed:",trade["Trader"])
            print()
            data = input("Do you accept this trade? (y/n) (or type q to quit): ")
            while(data.upper() != 'Q' and data.upper() != 'Y' and data.upper() != 'N'):
                data = input("Invalid command. Do you accept this trade? (y/n) (or type q to quit): ")
            if(data.upper() == "Y"):
                connection.close(roomName)
                return trade["Trader"]
            elif(data.upper() == "N" or data.upper() == "Q"):
                trade["Proposed"] = {"Name":"Empty","WeaponBouns":{"Health":0,"Attack":0,"Defense":0,"Speed":0,"Type":"SXLMA"}}
                connection.pushGame(roomName,trade)
                connection.passTurn(roomName,(positon % roomSize) + 1)
    except KeyboardInterrupt:
        connection.close(roomName)
        return -1
    connection.close(roomName)
    return -1
  
#START#

conn = LoginConnection()
info = begin(conn)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def dict2Character(d):
    if(d == "Empty"):
        return None
    name = d["Name"]
    style = d["Style"]
    weapon = d["Weapon"]["Name"]
    weaponbonus = (d["Weapon"]["Health"],d["Weapon"]["Attack"],d["Weapon"]["Defense"],d["Weapon"]["Speed"],d["Weapon"]["Type"])
    maxhealth = d["MaxHealth"]
    health = d["Health"]
    attack = d["Attack"]
    defense = d["Defense"]
    speed = d["Speed"]
    money = d["Money"]
    stash = d["Stash"]
    loc = [d["location"][0], d["location"][1], d["location"][2]]
    character = Character(Name=name, Style=style, Weapon=weapon, WeaponBonus=weaponbonus, Health=health, Attack=attack, Defense=defense, Speed=speed, Money=money,Stash=stash, location=loc)
    character.MaxHealth = maxhealth

    return character

def dict2Board(d):
    board = Board(size=len(d["Board"]),board=d["Board"])
    team1 = [None for i in range(5)]
    team2 = [None for i in range(5)]
    print(d["Team1"][0])
    index = 0
    for character in d["Team1"]:
        team1[index] = dict2Character(d["Team1"][index])
        index = index + 1

    index = 0
    for character in d["Team2"]:
        team2[index] = dict2Character(d["Team2"][index])
        index = index + 1

    return [board, team1, team2]

def JoinFight(character):
    #Colors
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[36m"
    end = "\033[0m"

    getch = _Getch()

    valid = "no"
    while(valid != 'Y'):      
        clear()
        b = Board()
        print("\t* * * * * * * * * * * * *")
        print("\t* * 1 * * * * * * * 4 * *")
        print("\t* * * * 2 * * * 3 * * * *")
        print("\t* * * * * * Y * * * * * *")
        print("\t* * * * * * * * * * * * *")
        print()
        print("Type in 4 character string represented the team you want for battle in order of positon (See Above)")
        print("([ex] \"ASXM\" for 1 Archer, 1 Swoardsmen, 1 Axeman, and 1 Mage)")
        setup = input("Team: ").upper()
        types = {'S','X','L','M','A'}
        while(len(setup) != 4):
            print("Invalid team command")
            setup = input("Team: ").upper()

        while(len(setup) != 4  or not ((setup[0] in types) and (setup[1] in types) and (setup[2] in types) and (setup[3] in types))):
            print("Invalid team command")
            setup = input("Team: ").upper()
            while(len(setup) != 4):
                print("Invalid team command")
                setup = input("Team: ").upper()

        print("\t* * * * * * * * * * * * *")
        print("\t* * " + setup[0] + " * * * * * * * " + setup[3] + " * *")
        print("\t* * * * " + setup[1] + " * * * " + setup[2] + " * * * *")
        print("\t* * * * * * Y * * * * * *")
        print("\t* * * * * * * * * * * * *")
        print()
        valid = input("Is this good (y/n)? ").upper()

    # Team 1
    team1 = [None, None, None, None, None]
    increments = [1,1,1,1,1]

    i = 0

    locations = [(12 - 1,10,'*'),(12 - 2,8,'*'),(12 - 3,6,'*'),(12 - 2,4,'*'),(12 - 1,2,'*')]
    for c in setup:
        if(c == "S"):
            team1[i] = Character(Name="Generic Swordsman " + str(increments[0]), Style="S", Weapon="Sword", WeaponBonus=(2,0,0,0,"S"), Health=50, Attack=50, Defense=30, Speed=15, Stash=["Sword1","Sword2","Sword3"],location=locations[i])
            b.place(team1[i].location,blue + "S" + end)
            increments[0] = increments[0] + 1
        if(c == "X"):
            team1[i] = Character(Name="Generic Axeman " + str(increments[1]), Style="X", Weapon="Axe", WeaponBonus=(0,2,0,0,"X"), Health=50, Attack=55, Defense=25, Speed=15, Stash=["Axeman1","Axeman2","Axeman3"],location=locations[i])
            b.place(team1[i].location,blue + "X" + end)
            increments[1] = increments[1] + 1
        if(c == "L"):
            team1[i] = Character(Name="Generic Lancer " + str(increments[2]), Style="L", Weapon="Lance", WeaponBonus=(0,0,2,0,"L"), Health=50, Attack=45, Defense=35, Speed=15, Stash=["Lance1","Lance2","Lance3"],location=locations[i])
            b.place(team1[i].location,blue + "L" + end)
            increments[2] = increments[2] + 1
        if(c == "M"):
            team1[i] = Character(Name="Generic Mage   " + str(increments[3]), Style="M", Weapon="The Magic Tome", WeaponBonus=(2,0,0,0,"M"), Health=52, Attack=53, Defense=30, Speed=10, Stash=["Book1","Book2","Book3"], location=locations[i])
            b.place(team1[i].location,blue + "M" + end)
            increments[3] = increments[3] + 1
        if(c == "A"):
            team1[i] = Character(Name="Generic Archer " + str(increments[4]), Style="A", Weapon="Bow", WeaponBonus=(0,2,0,0,"A"), Health=50, Attack=50, Defense=25, Speed=20, Stash=["Archer1","Archer2","Archer3"],location=locations[i])
            b.place(team1[i].location,blue + "A" + end)
            increments[4] = increments[4] + 1

        i = i + 1
        if(i == 2):
            i = i + 1

    character.Health = character.Health + character.WeaponBonus[0]
    team1[2] = character
    team1[2].location = locations[2]
    b.place(team1[2].location,blue + "&" + end)

    connection = MultiplayerConnection()
    clear()
    print()
    print("Connection Setup For Fight")
    print()
    roomName = input("Enter Room Name: ")
    playerName = "Player2"

    results = connection.join(roomName,playerName)
    while(results < 0):
        if(results == -1):
            roomName = input("Enter Room Name Again: ")
        elif(results == -2):
            playerName = input("Enter Player Name Again: ")
        results = connection.join(roomName,playerName)

    positon = results
    roomSize = connection.getRoomSize(roomName)
    
    content = dict2Board(connection.getGame(roomName))
    p1_board = content[0]
    team2 = content[1]

    for c in team2:
        b.place(c.location,red + c.getIcon() + end)

    connection.pushGame(roomName,b.board2dict(team2,team1))
    data = "start"

    connection.passTurn(roomName,(positon % roomSize) + 1)
    team1Win = False
    team2Win = False
    try:  
        while(not team1Win and not team2Win):
            clear()
            print()
            b.show()
            
            if(not(None in team1)):
                 print("{Team1}\n")
                for c in team1:
                    print(c.getStats())
                print()

            if(not(None in team2)):
                print("{Team2}\n")
                for c in team2:
                    print(c.getStats())

            print()
            connection.waitTurn(roomName,positon)
            clear()
            contents = dict2Board(connection.getGame(roomName))
            b = contents[0]
            team1 = contents[1]
            team2 = contents[2]

            clear()
            print()
            b.show()
            print()

            print("{Team1}\n")
            for c in team1:
                print(c.getStats())
            print()

            print("{Team2}\n")
            for c in team2:
                print(c.getStats())

            print()
            
             #Character
            team1Moved = []
            team2Moved = []

            for i in range(len(team1)):
                team1Moved.append(not team1[i].isAlive())
                    

            for i in range(len(team2)):
                team2Moved.append(not team2[i].isAlive())

            for char in team2:
                team1, team2, team2Moved = b.move(team1, team2, team2Moved, 2)
                
                if(not team1[int(len(team1)/2)].isAlive()):
                    team1Win = True
                    break
                
                if(not team2[int(len(team2)/2)].isAlive()):
                    team2Win = True
                    break

                for i in range(len(team1)):
                    if(not team1[i].isAlive()):
                        team1Moved[i] = True  

                for i in range(len(team2)):
                    if(not team2[i].isAlive()):
                        team2Moved[i] = True

            connection.pushGame(roomName,b.board2dict(team1,team2))
            connection.passTurn(roomName,(positon % roomSize) + 1)
    except:
        try:
            connection.close(roomName)
        except:
            pass
        return -1

    try:
        #print board
        clear()
        print()
        b.show()
        print()

        print("{Team1}\n")
        for c in team1:
            print(c.getStats())
        print()

        print("{Team2}\n")
        for c in team2:
            print(c.getStats())
        print()
    except:
        pass

    if(team1Win):
        print("You Win")
    if(team2Win):
        print("You Lost")
        try:
            connection.close(roomName)
        except:
            pass
        return 0


def StartFight(character):
    #Colors
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[36m"
    end = "\033[0m"

    getch = _Getch()

    valid = "no"
    while(valid != 'Y'):      
        clear()
        b = Board()
        print("\t* * * * * * * * * * * * *")
        print("\t* * 1 * * * * * * * 4 * *")
        print("\t* * * * 2 * * * 3 * * * *")
        print("\t* * * * * * Y * * * * * *")
        print("\t* * * * * * * * * * * * *")
        print()
        print("Type in 4 character string represented the team you want for battle in order of positon (See Above)")
        print("([ex] \"ASXM\" for 1 Archer, 1 Swoardsmen, 1 Axeman, and 1 Mage)")
        setup = input("Team: ").upper()
        types = {'S','X','L','M','A'}
        while(len(setup) != 4):
            print("Invalid team command")
            setup = input("Team: ").upper()

        while(len(setup) != 4  or not ((setup[0] in types) and (setup[1] in types) and (setup[2] in types) and (setup[3] in types))):
            print("Invalid team command")
            setup = input("Team: ").upper()
            while(len(setup) != 4):
                print("Invalid team command")
                setup = input("Team: ").upper()

        print("\t* * * * * * * * * * * * *")
        print("\t* * " + setup[0] + " * * * * * * * " + setup[3] + " * *")
        print("\t* * * * " + setup[1] + " * * * " + setup[2] + " * * * *")
        print("\t* * * * * * Y * * * * * *")
        print("\t* * * * * * * * * * * * *")
        print()
        valid = input("Is this good (y/n)? ").upper()

    # Team 1
    team1 = [None, None, None, None, None]
    increments = [1,1,1,1,1]

    i = 0
    locations = [(1,2,'*'),(2,4,'*'),(3,6,'*'),(2,8,'*'),(1,10,'*')]
    for c in setup:
        if(c == "S"):
            team1[i] = Character(Name="Generic Swordsman " + str(increments[0]), Style="S", Weapon="Sword", WeaponBonus=(2,0,0,0,"S"), Health=50, Attack=50, Defense=30, Speed=15, Stash=["Sword1","Sword2","Sword3"],location=locations[i])
            b.place(team1[i].location,red + "S" + end)
            increments[0] = increments[0] + 1
        if(c == "X"):
            team1[i] = Character(Name="Generic Axeman " + str(increments[1]), Style="X", Weapon="Axe", WeaponBonus=(0,2,0,0,"X"), Health=50, Attack=55, Defense=25, Speed=15, Stash=["Axeman1","Axeman2","Axeman3"],location=locations[i])
            b.place(team1[i].location,red + "X" + end)
            increments[1] = increments[1] + 1
        if(c == "L"):
            team1[i] = Character(Name="Generic Lancer " + str(increments[2]), Style="L", Weapon="Lance", WeaponBonus=(0,0,2,0,"L"), Health=50, Attack=45, Defense=35, Speed=15, Stash=["Lance1","Lance2","Lance3"],location=locations[i])
            b.place(team1[i].location,red + "L" + end)
            increments[2] = increments[2] + 1
        if(c == "M"):
            team1[i] = Character(Name="Generic Mage   " + str(increments[3]), Style="M", Weapon="The Magic Tome", WeaponBonus=(2,0,0,0,"M"), Health=52, Attack=53, Defense=30, Speed=10, Stash=["Book1","Book2","Book3"], location=locations[i])
            b.place(team1[i].location,red + "M" + end)
            increments[3] = increments[3] + 1
        if(c == "A"):
            team1[i] = Character(Name="Generic Archer " + str(increments[4]), Style="A", Weapon="Bow", WeaponBonus=(0,2,0,0,"A"), Health=50, Attack=50, Defense=25, Speed=20, Stash=["Archer1","Archer2","Archer3"],location=locations[i])
            b.place(team1[i].location,red + "A" + end)
            increments[4] = increments[4] + 1

        i = i + 1
        if(i == 2):
            i = i + 1

    character.Health = character.Health + character.WeaponBonus[0]
    team1[2] = character
    team1[2].location = locations[2]
    b.place(team1[2].location,red + "&" + end)

    team2 = [None, None, None, None, None]

    # Starting Connection
    connection = MultiplayerConnection()
    clear()
    print()
    print("Connection Setup For Fight")
    print()
    roomName = input("Enter Room Name: ")
    playerName = "Player1"
    roomSize = 2

    try:   
        results = connection.start(roomName,playerName,roomSize,game=b.board2dict(team1,team2))
        while(results == -1):
            roomName = input("Enter Room Name Again: ")
            results = connection.start(roomName,playerName,roomSize,game=b.board2dict(team1,team2))
    except:
        try:
            connection.close(roomName)
        except:
            pass
        return -1
    data = "Waiting"
    team1Win = False
    team2Win = False
    try:
        while(not team1Win and not team2Win):
            clear()
            print()
            b.show()

            if(not(None in team1)):
                 print("{Team1}\n")
                for c in team1:
                    print(c.getStats())
                print()

            if(not(None in team2)):
                print("{Team2}\n")
                for c in team2:
                    print(c.getStats())

            print()
            connection.waitTurn(roomName,1)
            clear()
            contents = dict2Board(connection.getGame(roomName))
            b = contents[0]
            team1 = contents[1]
            team2 = contents[2]

            clear()
            print()
            b.show()
            print()

            print("{Team1}\n")
            for c in team1:
                print(c.getStats())
            print()

            print("{Team2}\n")
            for c in team2:
                print(c.getStats())

            print()
            
             #Character
            team1Moved = []
            team2Moved = []

            for i in range(len(team1)):
                team1Moved.append(not team1[i].isAlive())
                    

            for i in range(len(team2)):
                team2Moved.append(not team2[i].isAlive())

            for char in team1:
                team1, team2, team1Moved = b.move(team1, team2, team1Moved, 1)
                
                if(not team1[int(len(team1)/2)].isAlive()):
                    team1Win = True
                    break
                
                if(not team2[int(len(team2)/2)].isAlive()):
                    team2Win = True
                    break
                
                for i in range(len(team1)):
                    if(not team1[i].isAlive()):
                        team1Moved[i] = True  

                for i in range(len(team2)):
                    if(not team2[i].isAlive()):
                        team2Moved[i] = True
            
            connection.pushGame(roomName,b.board2dict(team1,team2))
            connection.passTurn(roomName,2)
    except:
        try:
            connection.close(roomName)
        except:
            pass
        return -1

    try:
        #print board
        clear()
        print()
        b.show()
        print()

        print("{Team1}\n")
        for c in team1:
            print(c.getStats())
        print()

        print("{Team2}\n")
        for c in team2:
            print(c.getStats())
        print()
    except:
        pass

    if(team2Win):
        print("You Win")

    if(team1Win):
        print("You Lost")
        try:
            connection.close(roomName)
        except:
            pass
        return 0

    return -1

def SelectionMenu():
    character = info[0]
    username = info[1]
    if(character == -1):
        quit()

    if(character.Health + character.WeaponBonus[0] <= 0):
        print("You Died")
        conn.db.delete("Profiles/" + username)
        quit()

    def menu():
        print("Commands:")
        print("\tHeal - Spend $100 to increase health")
        print("\tBuy - Spend $1000 to get new Weapon")
        print("\tFight - Start 1v1 Battle with friend")
        print("\tEquip - Equip Weapon from stash")
        print("\tTrade [Unstable] - Weapons from stash via Room Names")
        print("\tClear - Clear Menu")
        print("\tSave - Save progress")
        print("\tQuit - Quit Menu")

    menu()
    command = input("&>> ").upper()
    while(command != 'Q' and command != 'QUIT'):
        if(command == 'HEAL'):
            print("Are sure you want to spend $100 to increase health to " + str(character.MaxHealth) + "? (y/n)")
            command = input("&>> ").upper()
            if(character.Money >= 100):
                if(character.Health < character.MaxHealth):
                    if(command == 'Y'):
                        character.Money = character.Money - 100
                        character.Health = character.MaxHealth
                        print("You are successfully healed")
                        print()
                        input("type anything to coninue... ")
                        conn.db.push("Profiles/" + username + "/Character", character.getDict())
                        clear()
                        character.show()
                        menu()
                else:
                    print("You are already at Max Health")
            else:
                print("You do not have enough money")
        if(command == 'BUY'):
            print("Are sure you want to spend $1000 on a new Weapon? (y/n)")
            command = input("&>> ").upper()
            if(character.Money >= 1000):
                if(command == 'Y'):
                    new_weapon = False
                    Weapon = None
                    while(new_weapon == False):
                        Weapon = LB.generate()
                        #print(Weapon)
                        new_weapon = True
                        for key, value in character.Stash.items():
                            if(key == Weapon[0]):
                                new_weapon = False
                    character.Money = character.Money - 1000
                    print("You Got:",Weapon)
                    print()
                    character.Stash[Weapon[0]] = {0:Weapon[1][0],1:Weapon[1][1],2:Weapon[1][2],3:Weapon[1][3],4:Weapon[1][4]}
                    conn.db.push("Profiles/" + username + "/Character", character.getDict())
                    input("type anything to coninue... ")
                    clear()
                    character.show()
                    menu()
            else:
                print("You do not have enough money")
        elif(command == 'FIGHT'):
            print("Type s to start fight and j to join")
            command = input("&>>  ")
            while(command.upper() != 'S' and command.upper() != 'J'):
                print("Invalid Choice. Type s to start fight and j to join")
                command = input("&>>  ")
            if(command.upper() == 'S'):
                result = StartFight(character)
            elif(command.upper() == 'J'):
                result = JoinFight(character)
            print()
            if(result != -1):
                if(result == 1):
                    character.Health = character.Health - character.WeaponBonus[0]

                    bonus_money = int(1500 * random.randint(50, 101)/100)
                    character.Money = character.Money + bonus_money
                    print("You gained $" + str(bonus_money))
                    conn.db.push("Profiles/" + username + "/Character", character.getDict())
                    input("type anything to continue... ")
                    clear()
                    character.show()
                    menu()
                if(result == 0):
                    clear()
                    character.show()
                    menu()
                    print("You Died")
                    conn.db.delete("Profiles/" + username)
                    quit()
            else:
                character.Health = character.Health - character.WeaponBonus[0]
                print("Game Broke")
                input("type anything to continue... ")
                clear()
                character.show()
                menu()
        elif(command == 'EQUIP'):
            weapon = False
            print("Type the name of the item you want to equiped")
            command = input("&>> ")
            for key, value in character.Stash.items():
                if(key == command):
                    weapon = True
            while(weapon == False and command.upper() != "Q" and command.upper() != "QUIT"):
                print("Item not found. Type the name of the item you want to equiped")
                command = input("&>> ")
                for key, value in character.Stash.items():
                    if(key == command):
                        weapon = True

            if(command.upper() != "Q" and command.upper() != "QUIT"):
                if(character.Style[0] in character.Stash[command][4] or character.Style[1] in character.Stash[command][4]):
                    if(character.Health + character.Stash[command][0] > 0 and character.Attack + character.Stash[command][1] > 0 and character.Defense + character.Stash[command][2] > 0 and character.Speed + character.Stash[command][3] > 0):
                        character.Stash[character.Weapon] = {0:character.WeaponBonus[0],1:character.WeaponBonus[1],2:character.WeaponBonus[2],3:character.WeaponBonus[3],4:character.WeaponBonus[4]}
                        character.Weapon = command
                        character.WeaponBonus = (character.Stash[command][0],character.Stash[command][1],character.Stash[command][2],character.Stash[command][3],character.Stash[command][4])
                        del character.Stash[command]
                        clear()
                        conn.db.push("Profiles/" + username + "/Character", character.getDict())
                        character.show()
                        menu()

                    else:
                        print("This item cannot make one of your stats less than 1")
                else:
                    print("Item cannot be equiped with your style")
        elif(command == 'TRADE'):
            print("Type in s to start trade or j to join trade via Room Name")
            command = input("&>> ")
            while(command.upper() != 'Q' and command.upper() != 'S' and command.upper() != 'J'):
                print("Invalid Command. Type in s to start trade or j to join trade via Room Name")
                command = input("&>> ")

            if(command.upper() == "S"):
                weapon = False
                print("Type the name of the item you want to trade")
                command = input("&>> ")
                for key, value in character.Stash.items():
                    if(key == command):
                        weapon = True
                while(weapon == False and command.upper() != "Q" and command.upper() != "QUIT"):
                    print("Item not found. Type the name of the item you want to trade")
                    command = input("&>> ")
                    for key, value in character.Stash.items():
                        if(key == command):
                            weapon = True

                if(command.upper() != "Q" and command.upper() != "QUIT"):
                    TWeapon = command
                    TWeaponBonus = {"Health":character.Stash[command][0],"Attack":character.Stash[command][1],"Defense":character.Stash[command][2],"Speed":character.Stash[command][3],"Type":character.Stash[command][4]}
                    #print("Type the details of the item/price you are looking for")
                    #command = input("&>> ")
                    if(command.upper() != "Q" and command.upper() != "QUIT"):
                        success = getTrade({"Name":TWeapon,"WeaponBonus":TWeaponBonus},command)
                        if(success != -1):
                            if(TWeapon != "Empty"):
                                del character.Stash[TWeapon]
                            character.Stash[success["Name"]] = {0:success["WeaponBonus"]["Health"],1:success["WeaponBonus"]["Attack"],2:success["WeaponBonus"]["Defense"],3:success["WeaponBonus"]["Speed"],4:success["WeaponBonus"]["Type"]}
                            character.Money = character.Money + success["Money"]
                            clear()
                            conn.db.push("Profiles/" + username + "/Character", character.getDict())
                            character.show()
                            menu()
                        else:
                            clear()
                            print()
                            print("Trade was unsuccessful")   
                            print()
                            conn.db.push("Profiles/" + username + "/Character", character.getDict())
                            character.show()
                            menu()  

            if(command.upper() == "J"):
                weapon = False
                print("Type the name of the item you want to trade or n for None")
                command = input("&>> ")
                for key, value in character.Stash.items():
                    if(key == command):
                        weapon = True
                while(weapon == False and command.upper() != "N"  and command.upper() != "Q" and command.upper() != "QUIT"):
                    print("Item not found. Type the name of the item you want to trade or n for None")
                    command = input("&>> ")
                    for key, value in character.Stash.items():
                        if(key == command):
                            weapon = True

                if(command.upper() != "Q" and command.upper() != "QUIT"):
                    TWeapon = "Empty"
                    TWeaponBonus = {"Health":0,"Attack":0,"Defense":0,"Speed":0,"Type":"SXLMA"}
                    if(command.upper() != "N"):
                        TWeapon = command
                        TWeaponBonus = {"Health":character.Stash[command][0],"Attack":character.Stash[command][1],"Defense":character.Stash[command][2],"Speed":character.Stash[command][3],"Type":character.Stash[command][4]}
                    print("Type the amount you want to trade")
                    command = input("&>> ")
                    while(int(command) > character.Money or int(command) < 0):
                        print("Invalid amount. Type the amount you want to trade (amount cannot be negative)")
                        print("You have $" + str(character.Money))
                        command = input("&>> ")

                    if(command.upper() != "Q" and command.upper() != "QUIT"):
                        success = joinTrade({"Name":TWeapon,"WeaponBonus":TWeaponBonus,"Money":int(command)})
                        print({"Name":TWeapon,"WeaponBonus":TWeaponBonus,"Money":0})
                        if(success != -1):
                            if(TWeapon != "Empty"):
                                del character.Stash[TWeapon]
                            character.Stash[success["Name"]] = {0:success["WeaponBonus"]["Health"],1:success["WeaponBonus"]["Attack"],2:success["WeaponBonus"]["Defense"],3:success["WeaponBonus"]["Speed"],4:success["WeaponBonus"]["Type"]}
                            character.Money = character.Money - int(command)
                            clear()
                            conn.db.push("Profiles/" + username + "/Character", character.getDict())
                            character.show()
                            menu()
                        else:
                            clear()
                            print()
                            print("Trade was unsuccessful")   
                            print()
                            conn.db.push("Profiles/" + username + "/Character", character.getDict())
                            character.show()
                            menu()  
        elif(command == 'CLEAR'):
            clear()
            character.show()
            menu()
        elif(command == 'SAVE'):
            conn.db.push("Profiles/" + username + "/Character", character.getDict())
            clear()
            character.show()
            menu()
        else:
            clear()
            character.show()
            menu()
            print("Invalid Command")
        command = input("&>> ").upper()

    conn.db.push("Profiles/" + username + "/Character", character.getDict())

SelectionMenu()