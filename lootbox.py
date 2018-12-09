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
            while(s1 == s2):
                s2 = random.choice(["S","X","L","M","A"])
            return s1 + s2
        else:
            return random.choice(["S","X","L","M","A"])


    def WeaponName(self,type):
        file = open("Names/test.txt", "r")
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

    def getLegendaryStats(self):
        stats = [0,0,0,0,None]
        perk1 = random.choice([10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10])
        perk2 = random.choice([10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10])
        perk3 = (perk2 * -1) + random.choice([5,4,3,2,1,0])
        perk4 = perk1 * -1
        perks = [perk1,perk2,perk3,perk4]
        stats[0] = perks[0]
        stats[1] = perks[1]
        stats[2] = perks[2]
        stats[3] = perks[3]
        return stats
    
    def getEpicStats(self):
        stats = [0,0,0,0,None]
        perk1 = random.choice([7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7])
        perk2 = random.choice([5,4,3,2,1,0,-1,-2,-3,-4,-5])
        perk3 = (perk2 * -1) + random.choice([3,2,1,0])
        perk4 = perk1 * -1
        perks = [perk1,perk2,perk3,perk4]
        random.shuffle(perks)
        stats[0] = perks[0]
        stats[1] = perks[1]
        stats[2] = perks[2]
        stats[3] = perks[3]
        return stats
    
    def getRareStats(self):
        stats = [0,0,0,0,None]
        perk1 = random.choice([5,4,3,2,1,0,-1,-2,-3,-4,-5])
        perk2 = random.choice([3,2,1,0,-1,-2,-3])
        perk3 = (perk2 * -1) + random.choice([2,1,0])
        perk4 = perk1 * -1
        perks = [perk1,perk2,perk3,perk4]
        random.shuffle(perks)
        stats[0] = perks[0]
        stats[1] = perks[1]
        stats[2] = perks[2]
        stats[3] = perks[3]
        return stats

    def getCommonStats(self):
        stats = [0,0,0,0,None]
        perk1 = random.choice([3,2,1,0,-1,-2,-3])
        perk2 = random.choice([2,1,0,-1,-2])
        perk3 = (perk2 * -1) + random.choice([1,0])
        perk4 = perk1 * -1
        perks = [perk1,perk2,perk3,perk4]
        random.shuffle(perks)
        stats[0] = perks[0]
        stats[1] = perks[1]
        stats[2] = perks[2]
        stats[3] = perks[3]
        return stats

        
    def WeaponStats(self):
        Common = self.getCommonStats()
        Rare = self.getRareStats()
        Epic = self.getEpicStats()
        Legendary = self.getLegendaryStats()
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
        self.Weapon[1] = self.WeaponStats()
        self.Weapon[0] = self.WeaponName(self.Weapon[1][4])
        return self.Weapon

LB = Lootbox()
print(LB.generate())