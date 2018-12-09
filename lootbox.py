from random import randint
import random
class Lootbox():
    def __init__(self):
        self.var = "LB"
        self.Weapon = ["name",[0,0,0,0,None]]
    
    def getType(self):
        val = randint(0,100)
        if(val < 30):
            s1 = random.choice(["S","X","L","M","A"])
            s2 = random.choice(["S","X","L","M","A"])
            while(s1 != s2):
                s2 = random.choice(["S","X","L","M","A"])
            return s1 + s2
        else:
            return random.choice(["S","X","L","M","A"])


    def WeaponName(self):
        file = open("test.txt", "r")
        contents = file.readlines()
        adjective = contents[0].split(", ")
        name = contents[1].split(", ")
        name2 = contents[2].split(", ")
        WeaponName = "" 
        if(self.val <= 59): 
            full_name = random.choice(adjective)+" "+random.choice(name)
            WeaponName = full_name
        else:
            full_name2 = random.choice(adjective)+" "+random.choice(name2)
            WeaponName = full_name2
        
        return WeaponName.replace("\n","")

        
    def WeaponStats(self):
        Common = [0,0,0,0,None]
        Rare = [1,1,1,1,None]
        Epic = [3,3,3,3,None]
        Legendary = [5,5,5,5,None]
        WeaponStats = ""
        if(self.val <= 59):
            WeaponStats = Common
            x = random.randint(0,3)
            Common[x] = Common[x] + 1
        if(self.val <= 89 and self.val > 59):
            WeaponStats = Rare
        if(self.val <= 99 and self.val > 89):
            WeaponStats = Epic
        if(self.val == 100):
            WeaponStats = Legendary
        WeaponStats[4] = self.getType()
        return WeaponStats

    def generate(self):
        self.val = randint(0,100)
        if(self.val <= 59):
            print("You Got a Common Weapon!")

        if(self.val <= 89 and self.val > 59):
            print("You Got a Rare Weapon!")
        if(self.val <= 99 and self.val > 89):
            print("You Got an Epic Weapon!")
        if(self.val == 100):
            print("You Got a Legendary Weapon!")
        self.Weapon[0] = self.WeaponName()
        self.Weapon[1] = self.WeaponStats()
        return self.Weapon
    







    