import os

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

    def num2hex(self,i):
        if(i < 10):
            return str(i)
        else:
            data = {
                10: 'A',
                11: 'B',
                12: 'C',
                13: 'D'
            }
            
            return data[i]

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

    def showStats(self):
        #print(self.Name + "\t[" + self.Style + ", " + self.Weapon + "]" + "\tHealth: " + str(self.Health) + "\nAttack: " + str(self.Attack) + "\tDefense: " + str(self.Defense) + "\tSpeed: " + str(self.Speed) + "\nMoney: " + str(self.Money))
        print("(" + self.num2hex(self.location[0]) + ", " + self.num2hex(self.location[1]) + ", " + self.location[2] + ") " + "[" +self.Style + "] " + self.Name + "\t| Health: " + str(self.Health) + " Attack: " + str(self.Attack) + " Speed: " + str(self.Speed) + " Defense: " + str(self.Defense))
  
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

    def num2hex(self,i):
        if(i < 10):
            return str(i)
        else:
            data = {
                10: 'A',
                11: 'B',
                12: 'C',
                13: 'D'
            }
            
            return data[i]

    def show(self):
        print("  0 1 2 3 4 5 6 7 8 9 A B C")
        for i in range(len(self.board)):
            print(self.num2hex(i) + ' ' + ' '.join(self.board[i]) + " " + self.num2hex(i))
        print("  0 1 2 3 4 5 6 7 8 9 A B C")

    def place(self,location,symbol):
        self.board[location[0]][location[1]] = symbol

    def swap(self,location1,location2):
        c = self.board[location1[0]][location1[1]]
        self.board[location1[0]][location1[1]] = self.board[location2[0]][location2[1]]
        self.board[location2[0]][location2[1]] = c

        
clear()
b = Board()

# Team 1
red = "\033[31m"
blue = "\033[36m"
end = "\033[0m"

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

print()
b.show()
print()

print("{Team1}\n")
gm.showStats()
gs.showStats()
gx.showStats()
gl.showStats()
ga.showStats()
print()

print("{Team2}\n")
gm2.showStats()
gs2.showStats()
gx2.showStats()
gl2.showStats()
ga2.showStats()
print()

# update board

# For each Character
## Move
## Exchange damage (Check if in range)(Calculate)
## See if death (if all dead win)

# push board
# Next playes turn

