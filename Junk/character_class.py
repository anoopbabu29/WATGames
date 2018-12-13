import os
import math

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