from random import randint
import random
class Lootbox():
    def __init__(self):
        self.var = "LB"
        self.Weapon = ["name",[0,0,0,0]]
    
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
        Common = [0,0,0,0]
        Rare = [1,1,1,1]
        Epic = [3,3,3,3]
        Legendary = [5,5,5,5]
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
    
    


    
        




#This is Test    
LB = Lootbox()
print(LB.generate())







    