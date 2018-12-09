from Multiplayer.Multiplayer import Database
from Character import Character
from lootbox import Lootbox
from uuid import getnode as get_mac
import os

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
        health = d["Health"]
        attack = d["Attack"]
        defense = d["Defense"]
        speed = d["Speed"]
        money = d["Money"]
        stash = d["Stash"]
        character = Character(Name=name, Style=style, Weapon=weapon, WeaponBonus=weaponbonus, Health=health, Attack=attack, Defense=defense, Speed=speed, Money=money,Stash=stash)

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
            pool = 30
            Health = 40
            Attack = 40
            Defense = 40
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

conn = LoginConnection()
info = begin(conn)
character = info[0]
username = info[1]
if(character == -1):
    quit()

def menu():
    print("Commands:")
    print("\tBuy - Spend $1000 to get new Weapon")
    print("\tFight - Start 1v1 Battle with friend")
    print("\tEquip - Equip Weapon from stash")
    print("\tClear - Clear Menu")
    print("\tSave - Save progress")
    print("\tQuit - Quit Menu")

menu()
command = input("&>> ").upper()
while(command != 'Q' and command != 'QUIT'):
    if(command == 'BUY'):
        print("Are sure you want to spend $1000 on a new Weapon? (y/n)")
        command = input("&>> ").upper()
        if(character.Money >= 1000):
            if(command == 'Y'):
                new_weapon = False
                Weapon = None
                while(new_weapon == False):
                    Weapon = LB.generate()
                    print(Weapon)
                    new_weapon = True
                    for key, value in character.Stash.items():
                        if(key == Weapon[0]):
                            new_weapon = False
                character.Money = character.Money - 1000
                print("You Got:",Weapon)
                print()
                input("type anything to coninue... ")
                character.Stash[Weapon[0]] = {0:Weapon[1][0],1:Weapon[1][1],2:Weapon[1][2],3:Weapon[1][3]}
                conn.db.push("Profiles/" + username + "/Character", character.getDict())
                clear()
                character.show()
                menu()
        else:
            print("You do not have enough money")
    elif(command == 'FIGHT'):
        print("Not Ready yet")
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
                if(character.Health + character.Stash[command][0] >= 0 and character.Attack + character.Stash[command][1] >= 0 and character.Defense + character.Stash[command][2] >= 0 and character.Speed + character.Stash[command][3] >= 0):
                    character.Stash[character.Weapon] = {0:character.WeaponBonus[0],1:character.WeaponBonus[1],2:character.WeaponBonus[2],3:character.WeaponBonus[3],4:character.WeaponBonus[4]}
                    character.Weapon = command
                    character.WeaponBonus = (character.Stash[command][0],character.Stash[command][1],character.Stash[command][2],character.Stash[command][3],character.Stash[command][4])
                    del character.Stash[command]
                    clear()
                    character.show()
                    menu()
                else:
                    print("This item cannot make one of your stats negative")
            else:
                print("Item cannot be equiped with your style")
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
        print("Invalid Command")
    command = input("&>> ").upper()

conn.db.push("Profiles/" + username + "/Character", character.getDict())