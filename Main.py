from Character import Character
from Character import Board
from Character import _Getch
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

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
        team1[i] = Character("Generic Swordsman " + str(increments[0]),"S", Stash=["Sword1","Sword2","Sword3"],location=locations[i])
        b.place(team1[i].location,red + "S" + end)
        increments[0] = increments[0] + 1
    if(c == "X"):
        team1[i] = Character("Generic Axeman " + str(increments[1]),"X", Stash=["Axeman1","Axeman2","Axeman3"],location=locations[i])
        b.place(team1[i].location,red + "X" + end)
        increments[1] = increments[1] + 1
    if(c == "L"):
        team1[i] = Character("Generic Lancer " + str(increments[2]),"L", Stash=["Lance1","Lance2","Lance3"],location=locations[i])
        b.place(team1[i].location,red + "L" + end)
        increments[2] = increments[2] + 1
    if(c == "M"):
        team1[i] = Character("Generic Mage   " + str(increments[3]),"M", Stash=["Book1","Book2","Book3"], location=locations[i])
        b.place(team1[i].location,red + "M" + end)
        increments[3] = increments[3] + 1
    if(c == "A"):
        team1[i] = Character("Generic Archer " + str(increments[4]),"A", Stash=["Archer1","Archer2","Archer3"],location=locations[i])
        b.place(team1[i].location,red + "A" + end)
        increments[4] = increments[4] + 1

    i = i + 1
    if(i == 2):
        i = i + 1

team1[2] = Character("This is You","MX", Attack=70, location=locations[2])
b.place(team1[2].location,red + "&" + end)

# Team 2

gm2 = Character("Generic Mage   ","M", Stash=["Book1","Book2","Book3"], location=(12 - 1,2,'*'))
b.place(gm2.location,blue + "M" + end)

gs2 = Character("Generic Swordsman","S", Stash=["Sword1","Sword2","Sword3"],location=(12 - 2,4,'*'))
b.place(gs2.location,blue + "S" + end)

gx2 = Character("Generic Axeman","X", Stash=["Axeman1","Axeman2","Axeman3"],location=(12 - 3,6,'*'))
b.place(gx2.location,blue + "X" + end)

gl2 = Character("Generic Lancer","L", Stash=["Lance1","Lance2","Lance3"],location=(12 - 2,8,'*'))
b.place(gl2.location,blue + "L" + end)

ga2 = Character("Generic Archer","A", Stash=["Archer1","Archer2","Archer3"],location=(12 - 1,10,'*'))
b.place(ga2.location,blue + "A" + end)

team2 = [gm2, gs2, gx2, gl2, ga2]

#

#ga2 = b.attack(gm,ga2)
print()
b.show()
print()

print("{Team1}\n")
for c in team1:
    print(c.getStats())
print()

print("{Team2}\n")
for c in team2:
    c.getStats()

print()

# update board

# For each Character
## Move
## Exchange damage (Check if in range)(Calculate)
## See if death (if all dead win)

# push board
# Next player's turn

cIn = ' '


while(ord(cIn) != 3):
    #Character
    team1Moved = [False, False, False, False, False]
    team2Moved = [False, False, False, False, False]
    
    for char in team1:
        team1, team2, team1Moved = b.move(team1, team2, team1Moved, 1)
    
    for char in team2:
        team1, team2, team2Moved = b.move(team1, team2, team2Moved, 2)