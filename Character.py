import os
import sys
import math

#Colors
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[36m"
end = "\033[0m"

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Character():
    def __init__(self, Name, Style, Weapon="None", WeaponBonus=(0,0,0,0,"SXLMA"), Health=40, Attack=40, Defense=40, Speed=15, Money=0, Stash={"Empty":{0:0,1:0,2:0,3:0,4:"SXLMA"}}, location=(None,None,None)):
        self.Name = Name
        self.Style = Style # S: Swordsman, X: Axeman, L: Lancer
        self.Weapon = Weapon
        self.WeaponBonus = WeaponBonus #(Health, Attack, Defense, Speed, Type)

        self.Health = Health
        self.Attack = Attack
        self.Defense = Defense
        self.Speed = Speed

        self.Money = Money
        self.Stash = Stash

        self.location = location

    def getIcon(self):
        if(len(self.Style) == 1):
            return self.Style
        return "&"

    def num2chr(self,i):
        if(i < 10):
            return str(i)
        else:
            return chr(i + 55)

    def getRange(self):
        return int(math.floor((self.Speed + self.WeaponBonus[3])/5))

    def show(self):
        #print(self.Name + "\t[" + self.Style + ", " + self.Weapon + "]" + "\tHealth: " + str(self.Health) + "\nAttack: " + str(self.Attack) + "\tDefense: " + str(self.Defense) + "\tSpeed: " + str(self.Speed) + "\nMoney: " + str(self.Money))
        
        print(self.Name + "\t\t$: " + str(self.Money))
        print("[" + self.Style + ", " + self.Weapon + "]")
        print("\n\tHealth: " + str(self.Health) + " + " + str(self.WeaponBonus[0]) + " \tAttack: " + str(self.Attack) + " + " + str(self.WeaponBonus[1]))
        print("\tSpeed: " + str(self.Speed) + " + " + str(self.WeaponBonus[3])  + "\tDefense: " + str(self.Defense) + " + " + str(self.WeaponBonus[2]))
        print("\tRange: " +  str(int(math.floor(self.Speed/5))) + " + " + str(self.getRange() - int(math.floor(self.Speed/5))))
        print()
        stash_str = "Stash [Health, Attack, Defense, Speed, Type]: "
        for key, value in self.Stash.items():
            stash_str = stash_str + key + "[" + str(value[0]) + ", " + str(value[1]) + ", " + str(value[2]) + ", " + str(value[3]) + ", " + str(value[4]) + "], "
        stash_str = stash_str

        print(stash_str[:-2])

    def getStats(self):
        #print(self.Name + "\t[" + self.Style + ", " + self.Weapon + "]" + "\tHealth: " + str(self.Health) + "\nAttack: " + str(self.Attack) + "\tDefense: " + str(self.Defense) + "\tSpeed: " + str(self.Speed) + "\nMoney: " + str(self.Money))
        return "(" + self.num2chr(self.location[0]) + ", " + self.num2chr(self.location[1]) + ", " + self.location[2] + ") " + "[" +self.Style + "] " + self.Name + "\t| Health: " + str(self.Health) + " Attack: " + str(self.Attack) + " Speed: " + str(self.Speed) + " Defense: " + str(self.Defense) + " Range: " + str(self.getRange())
  
    def getDict(self):
        return {
            "Name" : self.Name,
            "Style" : self.Style,
            "Weapon" : {
                "Name" : self.Weapon,
                "Health" : self.WeaponBonus[0],
                "Attack" : self.WeaponBonus[1],
                "Defense" : self.WeaponBonus[2],
                "Speed" : self.WeaponBonus[3],
                "Type" : self.WeaponBonus[4]
            },
            "Health" : self.Health,
            "Attack" : self.Attack,
            "Defense" : self.Defense,
            "Speed" : self.Speed,
            "Money" : self.Money,
            "Stash" : self.Stash,
            "location" : {"0" : self.location[0], "1" : self.location[1], "2" : self.location[2]}
        }
              
class Board():
    def __init__(self):
        self.size = 13
        self.board = []
        for i in range(self.size):
            self.board.append(['*']*self.size)

    def num2chr(self,i):
        if(i < 10):
            return str(i)
        else:
            return chr(i + 55)

    def show(self):
        axis = " "
        for i in range(self.size):
            axis = axis + " " + self.num2chr(i)
        print(axis)
        for i in range(self.size):
            print(self.num2chr(i) + ' ' + ' '.join(self.board[i]) + " " + self.num2chr(i))
        print(axis)

    def place(self,location,symbol):
        self.board[location[0]][location[1]] = symbol

    def swap(self,character,location2, color):
        c =  self.board[location2[0]][location2[1]]
        self.board[character.location[0]][character.location[1]] = character.location[2]
        self.place(location2, color + character.getIcon() + end)
        character.location = [location2[0], location2[1], c]
        return character

    def selChar(self, team, isMoved, i, o):      
        l = -1
        
        orde = range(len(isMoved))
        order = [((x + i) % (len(isMoved))) for x in orde]

        if(o == 0):
            order = order[::-1]

        for j in order:
            if(not isMoved[j]):
                l = j
                break
        
        if(l == -1):
            return None
        
        if(not isMoved[l]):
            character = team[l]
            self.board[character.location[0]][character.location[1]] = yellow + character.getIcon() + end

            return character, l
        else:
            return None


    def moveChar(self, team1, team2, isMoved, teamNum, l):
        team = []
        color = ''
        if(teamNum == 1):
            team = team1
            color = red
        elif(teamNum == 2):
            team = team2
            color = blue
        
        selPos = [team[l].location[0], team[l].location[1]]
        selChar = self.board[team[l].location[0]][team[l].location[1]]

        
        
        

        
        while(True):
            self.board[team[l].location[0]][team[l].location[1]] = green + team[l].getIcon() + end
            #print board
            clear()
            print()
            self.show()
            print()

            print("{Team1}\n")
            for i in range(len(team1)):
                if(i != l or teamNum != 1):
                    print(team1[i].getStats())
                else:
                    print(green + team1[i].getStats() + end)
            print()

            print("{Team2}\n")
            for i in range(len(team1)):
                if(i != l or teamNum != 2):
                    print(team2[i].getStats())
                else:
                    print(green + team2[i].getStats() + end)
            print()

            #Get Input
            ch = getch.__call__()
            print(str(ch) + ": " + str(ord(ch)))
            if(ord(ch) == 3):
                sys.exit(0)
            elif(ord(ch) == 27):
                self.board[team[l].location[0]][team[l].location[1]] = yellow + team[l].getIcon() + end
                self.board[selPos[0]][selPos[1]] = selChar
                break
            elif(ord(ch) == 13):
                #Pressed Enter
                if(self.board[selPos[0]][selPos[1]] == (green + '*' + end)): 
                    self.board[team[l].location[0]][team[l].location[1]] = color + team[l].getIcon() + end
                    self.board[selPos[0]][selPos[1]] = selChar
                    self.swap(team[l], selPos, color)
                    isMoved[l] = True
                    break
                elif(self.board[selPos[0]][selPos[1]] == (green + team[l].getIcon() + end)):
                    self.board[team[l].location[0]][team[l].location[1]] = color + team[l].getIcon() + end
                    isMoved[l] = True
                    break
                    
            elif(ord(ch) == 119):
                #Move Up if possible
                dist = abs((selPos[0] - 1) - team[l].location[0]) + abs((selPos[1]) - team[l].location[1])
                if(selPos[0] - 1 >= 0 and dist <= team[l].getRange()):
                    self.board[selPos[0]][selPos[1]] = selChar
                    selPos = [selPos[0] - 1, selPos[1]]
                    selChar = self.board[selPos[0]][selPos[1]]
                    self.board[selPos[0]][selPos[1]] = green + selChar + end

            elif(ord(ch) == 97):
                #Move Left if possible
                dist = abs((selPos[0]) - team[l].location[0]) + abs((selPos[1] - 1) - team[l].location[1])
                if(selPos[1] - 1 >= 0 and dist <= team[l].getRange()):
                    self.board[selPos[0]][selPos[1]] = selChar
                    selPos = [selPos[0], selPos[1] - 1]
                    selChar = self.board[selPos[0]][selPos[1]]
                    self.board[selPos[0]][selPos[1]] = green + selChar + end
            elif(ord(ch) == 115):
                #Move Down if possible
                dist = abs((selPos[0] + 1) - team[l].location[0]) + abs((selPos[1]) - team[l].location[1])
                if(selPos[0] + 1 <= (len(self.board) - 1) and dist <= team[l].getRange()):
                    self.board[selPos[0]][selPos[1]] = selChar
                    selPos = [selPos[0] + 1, selPos[1]]
                    selChar = self.board[selPos[0]][selPos[1]]
                    self.board[selPos[0]][selPos[1]] = green + selChar + end
            elif(ord(ch) == 100):
                #Move Right if possible
                dist = abs((selPos[0]) - team[l].location[0]) + abs((selPos[1] + 1) - team[l].location[1])
                if((selPos[1] + 1 <= len(self.board[selPos[0]]) - 1) and dist <= team[l].getRange()):
                    self.board[selPos[0]][selPos[1]] = selChar
                    selPos = [selPos[0], selPos[1] + 1]
                    selChar = self.board[selPos[0]][selPos[1]]
                    self.board[selPos[0]][selPos[1]] = green + selChar + end
        
        if(teamNum == 1):
            team1 = team
        elif(teamNum == 2):
            team2 = team
        
        return team1, team2, isMoved

        

    def move(self, team1, team2, isMoved, teamNum):
        team = []
        if(teamNum == 1):
            team = team1
            color = red
        elif(teamNum == 2):
            team = team2
            color = blue
        
        selCharacter, l = self.selChar(team, isMoved, 0, 1)
        while(not isMoved[l]):
            #print board
            clear()
            print()
            self.show()
            print()

            print("{Team1}\n")
            for i in range(len(team1)):
                if(i != l or teamNum != 1):
                    print(team1[i].getStats())
                else:
                    print(yellow + team1[i].getStats() + end)
            print()

            print("{Team2}\n")
            for i in range(len(team1)):
                if(i != l or teamNum != 2):
                    print(team2[i].getStats())
                else:
                    print(yellow + team2[i].getStats() + end)
            print()
            
            #Character Selection
            ch = getch.__call__()
            #Left Input
            if(ord(ch) == 97):
                self.board[selCharacter.location[0]][selCharacter.location[1]] = color + selCharacter.getIcon() + end
                selCharacter, l = self.selChar(team, isMoved, (l), 0)
            elif(ord(ch) == 100):
                self.board[selCharacter.location[0]][selCharacter.location[1]] = color + selCharacter.getIcon() + end
                selCharacter, l = self.selChar(team, isMoved, (l + 1) , 1)
            #Select Char
            elif(ord(ch) == 13):
                #Actually move character
                team1, team2, isMoved = self.moveChar(team1, team2, isMoved, teamNum, l)
            elif(ord(ch) == 3):
                sys.exit(0)
        
        if(teamNum == 1):
            team1 = team
        elif(teamNum == 2):
            team2 = team
        
        return team1, team2, isMoved

    def bonus(self,attacker,defender):
        bonus = 0
        if(("S" in attacker.Style and "X" in defender.Style) or ("X" in attacker.Style and "L" in defender.Style) or ("L" in attacker.Style and "S" in defender.Style) or ("M" in attacker.Style and "A" in defender.Style) or ("A" in attacker.Style and "M" in defender.Style)):
            bonus = bonus + 0.2

        if(("X" in attacker.Style and "S" in defender.Style) or ("L" in attacker.Style and "X" in defender.Style) or ("S" in attacker.Style and "L" in defender.Style)):
            bonus = bonus - 0.2
        
        return 1 + bonus

    def attack(self,attacker,defender):
        damage = ((attacker.Attack + attacker.WeaponBonus[1]) - (defender.Defense + defender.WeaponBonus[2])) * self.bonus(attacker,defender)
        defender.Health = int((defender.Health - damage) * math.floor(attacker.Speed/defender.Speed))
        return defender

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