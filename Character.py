import os
import sys
import math

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#Colors
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[36m"
purple = "\033[35m"
dblue = "\033[94m"
lblue = "\033[96m"
end = "\033[0m"

GREY    = '\33[90m'
CRED2    = '\33[91m'
CGREEN2  = '\33[92m'
CYELLOW2 = '\33[93m'
CBLUE2   = '\33[94m'
CVIOLET2 = '\33[95m'
CBEIGE2  = '\33[96m'
CWHITE2  = '\33[97m'

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

class Character():
    def __init__(self, Name, Style, Weapon="None", WeaponBonus=(0,0,0,0,"SXLMA"), Health=40, Attack=40, Defense=20, Speed=5, Money=0, Stash={"Empty":{0:0,1:0,2:0,3:0,4:"SXLMA"}}, location=[None,None,None]):
        self.Name = Name
        self.Style = Style # S: Swordsman, X: Axeman, L: Lancer
        self.EquipedStyle = None
        if(len(Style) == 1):
            self.EquipedStyle = self.Style
        else:
            self.EquipedStyle = self.Style[0]

        self.Weapon = Weapon
        self.WeaponBonus = WeaponBonus #(Health, Attack, Defense, Speed, Type)

        self.MaxHealth = Health
        self.Health = Health
        self.Attack = Attack
        self.Defense = Defense
        self.Speed = Speed

        self.Money = Money
        self.Stash = Stash

        self.location = location

    def isAlive(self):
        if(self.Health <= 0):
            return False
        return True

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
        
        print(CVIOLET2 + self.Name + end + "\t\t\t$: " + green + str(self.Money) + end)
        print(GREY + "[" + self.Style + ", " + self.Weapon + "]" + end)
        print(green + "\n\tHealth: " + end + str(self.Health) + " + " + str(self.WeaponBonus[0]) + red + " \tAttack: " + end + str(self.Attack) + " + " + str(self.WeaponBonus[1]))
        print(yellow + "\tSpeed: " + end + str(self.Speed) + " + " + str(self.WeaponBonus[3])  + blue + "\tDefense: " + end + str(self.Defense) + " + " + str(self.WeaponBonus[2]))
        print(purple + "\tRange: " + end + str(int(math.floor(self.Speed/5))) + " + " + str(self.getRange() - int(math.floor(self.Speed/5))))
        print()
        stash_str = GREY + "Stash: " + end
        for key, value in self.Stash.items():
            stash_str = stash_str + key + " [" + green + str(value[0]) + end + ", " + red + str(value[1]) + end + ", " + blue + str(value[2]) + end + ", " + yellow + str(value[3]) + end +  ", " + str(value[4]) + "], "
        stash_str = stash_str

        print(stash_str[:-2])

    def getStats(self):
        #print(self.Name + "\t[" + self.Style + ", " + self.Weapon + "]" + "\tHealth: " + str(self.Health) + "\nAttack: " + str(self.Attack) + "\tDefense: " + str(self.Defense) + "\tSpeed: " + str(self.Speed) + "\nMoney: " + str(self.Money))
        if(self.Health < 0):
            return red + "{ Dead } " + "[" +self.Style + "] " + self.Name + "\t| Health: " + str(self.Health) + " Attack: " + str(self.Attack + self.WeaponBonus[1]) + " Speed: " + str(self.Speed + self.WeaponBonus[3]) + " Defense: " + str(self.Defense + self.WeaponBonus[2]) + " Range: " + str(self.getRange()) + end
  
        return "(" + self.num2chr(self.location[0]) + ", " + self.num2chr(self.location[1]) + ", " + self.location[2] + ") " + "[" +self.Style + "] " + self.Name + "\t| Health: " + str(self.Health) + " Attack: " + str(self.Attack + self.WeaponBonus[1]) + " Speed: " + str(self.Speed + self.WeaponBonus[3]) + " Defense: " + str(self.Defense + self.WeaponBonus[2]) + " Range: " + str(self.getRange())
  
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
            "MaxHealth" : self.MaxHealth,
            "Health" : self.Health,
            "Attack" : self.Attack,
            "Defense" : self.Defense,
            "Speed" : self.Speed,
            "Money" : self.Money,
            "Stash" : self.Stash,
            "location" : {0 : self.location[0], 1 : self.location[1], 2 : self.location[2]}
        }

class Board():
    def __init__(self,size=13,board=[]):
        self.size = size
        self.board = board
        if board == []:
            for i in range(self.size):
                self.board.append(['*']*self.size)

    def board2dict(self,team1,team2):
        board = {
            "Board":self.board,
            "Team1": {},
            "Team2": {}
        }
        index = 0
        for character in team1:
            if(character == None):
                board["Team1"][index] = "Empty"
            else:
                board["Team1"][index] = character.getDict()
            index = index + 1

        index = 0
        for character in team2:
            if(character == None):
                board["Team2"][index] = "Empty"
            else:
                board["Team2"][index] = character.getDict()
            index = index + 1
        return board

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

    def get_adjacent_cells(self, x_coord, y_coord, r):
        result = {}
        if(r == 1):
            for x,y in [(x_coord+i,y_coord+j) for i in (-1,0,1) for j in (-1,0,1) if (i != 0 or j != 0) and (i == 0 or j == 0)]:
                result[(x,y)] = True
        elif(r == 2):
            for x,y in [(x_coord+i,y_coord+j) for i in (-1,0,1) for j in (-1,0,1) if (i != 0 or j != 0) and (i == 0 or j == 0)]:
                result[(x,y)] = True

            temp = result.copy()
            for key, value in temp.items():
                x_coord = key[0]
                y_coord = key[1]
                for x,y in [(x_coord+i,y_coord+j) for i in (-1,0,1) for j in (-1,0,1) if (i != 0 or j != 0) and (i == 0 or j == 0)]:
                    result[(x,y)] = True

        return result

    def inRadius(self, attacker, defender):
        astyle = attacker.Style
        if(len(attacker.Style) > 1):
            astyle = attacker.EquipedStyle

        if(astyle in {'S','X','L'}):
            print((attacker.location, defender.location))
            attack_zone = self.get_adjacent_cells(attacker.location[0],attacker.location[1],1)
            if((defender.location[0],defender.location[1]) in attack_zone):
                return True
            else:
                return False
        
        if(astyle in {'M'}):
            print((attacker.location, defender.location))
            attack_zone = self.get_adjacent_cells(attacker.location[0],attacker.location[1],2)
            if((defender.location[0],defender.location[1]) in attack_zone):
                return True
            else:
                return False

        if(astyle in {'A'}):
            print((attacker.location, defender.location))
            print(2," -",1)
            attack_zone = self.get_adjacent_cells(attacker.location[0],attacker.location[1],2)
            close_zone = self.get_adjacent_cells(attacker.location[0],attacker.location[1],1)
            if(((defender.location[0],defender.location[1]) in attack_zone) and not ((defender.location[0],defender.location[1]) in close_zone)):
                return True
            else:
                return False

    def inAttackRadius(self,attacker,defender):
        astyle = attacker.Style
        if(len(attacker.Style) > 1):
            astyle = attacker.EquipedStyle

        if(astyle in {'S','X','L'}):
            print((attacker.location, defender.location))
            attack_zone = self.get_adjacent_cells(attacker.location[0],attacker.location[1],1)
            if((defender.location[0],defender.location[1]) in attack_zone):
                return self.attack(attacker,defender)
            else:
                return -1
        
        if(astyle in {'M'}):
            print((attacker.location, defender.location))
            attack_zone = self.get_adjacent_cells(attacker.location[0],attacker.location[1],2)
            if((defender.location[0],defender.location[1]) in attack_zone):
                return self.attack(attacker,defender)
            else:
                return -1

        if(astyle in {'A'}):
            print((attacker.location, defender.location))
            print(2," -",1)
            attack_zone = self.get_adjacent_cells(attacker.location[0],attacker.location[1],2)
            close_zone = self.get_adjacent_cells(attacker.location[0],attacker.location[1],1)
            if(((defender.location[0],defender.location[1]) in attack_zone) and not ((defender.location[0],defender.location[1]) in close_zone)):
                return self.attack(attacker,defender)
            else:
                return -1

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
            return team[0], 0
        
        if(not isMoved[l]):
            character = team[l]
            self.board[character.location[0]][character.location[1]] = yellow + character.getIcon() + end

            return character, l
        else:
            return team[0], 0


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


    def attackStep(self, team1, team2, teamNum, l):
        ateam = []
        dteam = []
        if(teamNum == 1):
            ateam = team1
            dteam = team2
            acolor = red
            dcolor = blue
        elif(teamNum == 2):
            ateam = team2
            dteam = team1
            acolor = blue
            dcolor = red
        
        selPos = [ateam[l].location[0], ateam[l].location[1]]

        selIndex = 0
        inRadius = []
        isNextTo = False
        for i in range(len(dteam)):
            if(self.inRadius(ateam[l], dteam[i])):
                inRadius.append(dteam[i])
                isNextTo = True
            else:
                inRadius.append(None)

        if(isNextTo):
            for i in range(len(inRadius)):
                if(inRadius[i] != None):
                    selIndex = i
                    break
            self.board[selPos[0]][selPos[1]] = green + ateam[l].getIcon() + end
            self.board[dteam[selIndex].location[0]][dteam[selIndex].location[1]] = yellow + dteam[selIndex].getIcon() + end
            self.board[ateam[l].location[0]][ateam[l].location[1]] = green + ateam[l].getIcon() + end
        
        while(isNextTo):
            #print board
            clear()
            print()
            self.show()
            print()

            print("{Team1}\n")
            for i in range(len(team1)):
                if(i == l and teamNum == 1):
                    print(green + team1[i].getStats() + end)
                elif(i == selIndex and teamNum == 2):
                    print(yellow + team1[i].getStats() + end)
                else:
                    print(team1[i].getStats())
            print()

            print("{Team2}\n")
            for i in range(len(team1)):
                if(i == l and teamNum == 2):
                    print(green + team2[i].getStats() + end)
                elif(i == selIndex and teamNum == 1):
                    print(yellow + team2[i].getStats() + end)
                else:
                    print(team2[i].getStats())
            print()

            #Get Input
            ch = getch.__call__()
            
            if(ord(ch) == 3):
                sys.exit(0)
            elif(ord(ch) == 27):
                self.board[dteam[selIndex].location[0]][dteam[selIndex].location[1]] = dcolor + dteam[selIndex].getIcon() + end
                self.board[selPos[0]][selPos[1]] = acolor + ateam[l].getIcon() + end
                break
            elif(ord(ch) == 13):
                #Pressed Enter
                self.board[dteam[selIndex].location[0]][dteam[selIndex].location[1]] = dcolor + dteam[selIndex].getIcon() + end
                self.board[ateam[l].location[0]][ateam[l].location[1]] = acolor + ateam[l].getIcon() + end

                dteam[selIndex] = self.inAttackRadius(ateam[l], dteam[selIndex])
                if(dteam[selIndex].isAlive()):
                    if(self.inRadius(dteam[selIndex], ateam[l])):
                        ateam[l] = self.inAttackRadius(dteam[selIndex], ateam[l])
                        if(not ateam[l].isAlive()):
                            self.board[ateam[l].location[0]][ateam[l].location[1]] = ateam[l].location[2]
                            ateam[l].location[0] = -99
                            ateam[l].location[1] = -99
                else:
                    self.board[dteam[selIndex].location[0]][dteam[selIndex].location[1]] = dteam[selIndex].location[2]
                    dteam[selIndex].location[0] = -99
                    dteam[selIndex].location[1] = -99
                break

            elif(ord(ch) == 97):
                #Select Left
                self.board[inRadius[selIndex].location[0]][inRadius[selIndex].location[1]] = dcolor + inRadius[selIndex].getIcon() + end
                selIndex = selIndex - 1
                if(selIndex == -1):
                    selIndex = len(inRadius) - 1
                while(inRadius[selIndex] == None):
                    selIndex = selIndex - 1
                    if(selIndex == -1):
                        selIndex = len(inRadius) - 1
                self.board[inRadius[selIndex].location[0]][inRadius[selIndex].location[1]] = yellow + inRadius[selIndex].getIcon() + end
            elif(ord(ch) == 100):
                #Select Right
                self.board[inRadius[selIndex].location[0]][inRadius[selIndex].location[1]] = dcolor + inRadius[selIndex].getIcon() + end
                selIndex = (selIndex + 1) % len(inRadius)
                while(inRadius[selIndex] == None):
                    selIndex = (selIndex + 1) % len(inRadius)
                self.board[inRadius[selIndex].location[0]][inRadius[selIndex].location[1]] = yellow + inRadius[selIndex].getIcon() + end
        
        if(teamNum == 1):
            team1 = ateam
            team2 = dteam
        elif(teamNum == 2):
            team2 = ateam
            team1 = dteam
        
        return team1, team2


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
                #Attack Step if Moved
                if(isMoved[l]):
                    team1, team2 = self.attackStep(team1, team2, teamNum, l)
            elif(ord(ch) == 3):
                sys.exit(0)
        
        if(teamNum == 1):
            team1 = team
        elif(teamNum == 2):
            team2 = team
        
        return team1, team2, isMoved