from Multiplayer.Multiplayer import Database, MultiplayerConnection
from Character import Character
from Character import Board
from Character import _Getch
from lootbox import Lootbox
from uuid import getnode as get_mac
import os
import random
import time
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
    exp = d["Experience"]
    money = d["Money"]
    stash = d["Stash"]
    loc = [d["location"][0], d["location"][1], d["location"][2]]
    character = Character(Name=name, Style=style, Weapon=weapon, WeaponBonus=weaponbonus, Health=health, Attack=attack, Defense=defense, Speed=speed, Money=money,Stash=stash, location=loc, Experience=exp)
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

def watch(connection,id):
    links = connection.db.get("Multiplayer")
    for key, value in links.items():
        if(key == id):
            connection.my_stream = connection.db.db.child("Multiplayer/" + str(id)).stream(connection.stream_handler)
            return 1
    return -1

#Colors
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[36m"
end = "\033[0m"

connection = MultiplayerConnection()
clear()
print()
print("Connection Setup For Fight View")
print()
roomName = input("Enter Room Name: ")
playerName = "Viwer"

results = watch(connection,roomName)
while(results < 0):
    if(results == -1):
        roomName = input("Enter Room Name Again: ")
    elif(results == -2):
        playerName = input("Enter Player Name Again: ")
    results = watch(connection,roomName)

positon = results
roomSize = connection.getRoomSize(roomName)

content = dict2Board(connection.getGame(roomName))
b = content[0]
team1 = content[1]
team2 = content[2]

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
            if(not team1[int(len(team1)/2)].isAlive()):
                team1Win = True
                break

        if(not(None in team2)):
            print("{Team2}\n")
            for c in team2:
                print(c.getStats())
            if(not team2[int(len(team2)/2)].isAlive()):
                team2Win = True
                break

        print()
        wait = True
        connection.dataChange = False
        while(wait):
            if connection.dataChange:
                #clear()
                #print("Room: " + id + "\n")
                print()
                #self.db.show("Multiplayer/" + str(id))
                print("Waiting for Player " + str(connection.db.get("Multiplayer/" + str(id) + "/Turn")))
                connection.dataChange = False
                wait = False

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
        if(not team1[int(len(team1)/2)].isAlive()):
            team1Win = True
            break
        print()

        print("{Team2}\n")
        for c in team2:
            print(c.getStats())
        if(not team2[int(len(team2)/2)].isAlive()):
            team2Win = True
            break
except:
    pass

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
    print("Team 2 Wins")

if(team2Win):
    print("Team 1 Wins")