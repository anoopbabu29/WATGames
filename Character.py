import os
import sys

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
    def __init__(self, Name, Style, Weapon="None", WeaponBonus=(0,0,0,0), Health=40, Attack=40, Defense=40, Speed=40, Money=0, Stash=["Empty"], location=(None,None,None)):
        self.Name = Name
        self.Style = Style # S: Swordsman, X: Axeman, L: Lancer
        self.Weapon = Weapon
        self.WeaponBonus = WeaponBonus

        self.Health = Health
        self.Attack = Attack
        self.Defense = Defense
        self.Speed = Speed

        self.Money = Money
        self.Stash = Stash

        self.location = location

    def num2chr(self,i):
        if(i < 10):
            return str(i)
        else:
            return chr(i + 55)

    def show(self):
        #print(self.Name + "\t[" + self.Style + ", " + self.Weapon + "]" + "\tHealth: " + str(self.Health) + "\nAttack: " + str(self.Attack) + "\tDefense: " + str(self.Defense) + "\tSpeed: " + str(self.Speed) + "\nMoney: " + str(self.Money))
        
        print(self.Name + "\t\t$: " + str(self.Money))
        print("[" + self.Style + ", " + self.Weapon + "]")
        print("\n\tHealth: " + str(self.Health) + "\tAttack: " + str(self.Attack))
        print("\tSpeed: " + str(self.Speed) + "\tDefense: " + str(self.Defense))
        print()
        stash_str = "Stash: "
        for item in self.Stash:
            stash_str = stash_str + item + ", "
        stash_str = stash_str

        print(stash_str[:-2])

    def getStats(self):
        #print(self.Name + "\t[" + self.Style + ", " + self.Weapon + "]" + "\tHealth: " + str(self.Health) + "\nAttack: " + str(self.Attack) + "\tDefense: " + str(self.Defense) + "\tSpeed: " + str(self.Speed) + "\nMoney: " + str(self.Money))
        return "(" + self.num2chr(self.location[0]) + ", " + self.num2chr(self.location[1]) + ", " + self.location[2] + ") " + "[" +self.Style + "] " + self.Name + "\t| Health: " + str(self.Health) + " Attack: " + str(self.Attack) + " Speed: " + str(self.Speed) + " Defense: " + str(self.Defense)
  
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
            },
            "Health" : self.Health,
            "Attack" : self.Attack,
            "Defense" : self.Defense,
            "Speed" : self.Speed,
            "Money" : self.Money,
            "Stash" : ','.join(self.Stash),
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
        self.place(location2, color + character.Style + end)
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
            self.board[character.location[0]][character.location[1]] = yellow + character.Style + end

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
            self.board[team[l].location[0]][team[l].location[1]] = green + team[l].Style + end
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
                self.board[team[l].location[0]][team[l].location[1]] = yellow + team[l].Style + end
                self.board[selPos[0]][selPos[1]] = selChar
                break
            elif(ord(ch) == 13):
                #Pressed Enter
                if(self.board[selPos[0]][selPos[1]] == (green + '*' + end) or self.board[selPos[0]][selPos[1]] == (green + team[l].Style + end)):
                    self.board[team[l].location[0]][team[l].location[1]] = color + team[l].Style + end
                    self.board[selPos[0]][selPos[1]] = selChar
                    self.swap(team[l], selPos, color)
                    isMoved[l] = True
                    break
            elif(ch == 'w'):
                #Move Up if possible
                if(selPos[0] - 1 >= 0):
                    self.board[selPos[0]][selPos[1]] = selChar
                    selPos = [selPos[0] - 1, selPos[1]]
                    selChar = self.board[selPos[0]][selPos[1]]
                    self.board[selPos[0]][selPos[1]] = green + selChar + end

            elif(ch == 'a'):
                #Move Left if possible
                if(selPos[1] - 1 >= 0):
                    self.board[selPos[0]][selPos[1]] = selChar
                    selPos = [selPos[0], selPos[1] - 1]
                    selChar = self.board[selPos[0]][selPos[1]]
                    self.board[selPos[0]][selPos[1]] = green + selChar + end
            elif(ch == 's'):
                #Move Down if possible
                if(selPos[0] + 1 <= len(self.board) - 1):
                    self.board[selPos[0]][selPos[1]] = selChar
                    selPos = [selPos[0] + 1, selPos[1]]
                    selChar = self.board[selPos[0]][selPos[1]]
                    self.board[selPos[0]][selPos[1]] = green + selChar + end
            elif(ch == 'd'):
                #Move Right if possible
                if(selPos[1] + 1 <= len(self.board[selPos[0]]) - 1):
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
            if(ch == 'a'):
                self.board[selCharacter.location[0]][selCharacter.location[1]] = color + selCharacter.Style + end
                selCharacter, l = self.selChar(team, isMoved, (l), 0)
            elif(ch == 'd'):
                self.board[selCharacter.location[0]][selCharacter.location[1]] = color + selCharacter.Style + end
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

clear()
b = Board()


# Team 1

gm = Character("Generic Mage   ","M", Stash=["Book1","Book2","Book3"],location=(1,2,'*'))
b.place(gm.location,red + "M" + end)

gs = Character("Generic Swordsman","S", Stash=["Sword1","Sword2","Sword3"],location=(2,4,'*'))
b.place(gs.location,red + "S" + end)

gx = Character("Generic Axeman","X", Stash=["Axeman1","Axeman2","Axeman3"],location=(3,6,'*'))
b.place(gx.location,red + "X" + end)

gl = Character("Generic Lancer","L", Stash=["Lance1","Lance2","Lance3"],location=(2,8,'*'))
b.place(gl.location,red + "L" + end)

ga = Character("Generic Archer","A", Stash=["Archer1","Archer2","Archer3"],location=(1,10,'*'))
b.place(ga.location,red + "A" + end)


# Team 2

gm2 = Character("Generic Mage   ","M", Stash=["Book1","Book2","Book3"],location=(12 - 1,2,'*'))
b.place(gm2.location,blue + "M" + end)

gs2 = Character("Generic Swordsman","S", Stash=["Sword1","Sword2","Sword3"],location=(12 - 2,4,'*'))
b.place(gs2.location,blue + "S" + end)

gx2 = Character("Generic Axeman","X", Stash=["Axeman1","Axeman2","Axeman3"],location=(12 - 3,6,'*'))
b.place(gx2.location,blue + "X" + end)

gl2 = Character("Generic Lancer","L", Stash=["Lance1","Lance2","Lance3"],location=(12 - 2,8,'*'))
b.place(gl2.location,blue + "L" + end)

ga2 = Character("Generic Archer","A", Stash=["Archer1","Archer2","Archer3"],location=(12 - 1,10,'*'))
b.place(ga2.location,blue + "A" + end)

team1 = [gm, gs, gx, gl, ga]
team2 = [gm2, gs2, gx2, gl2, ga2]

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
    