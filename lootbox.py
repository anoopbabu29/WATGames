from random import randint
import random

from collections import OrderedDict

class Lootbox():
    def __init__(self):
        self.var = "LB"
        self.Weapon = ["name",[0,0,0,0,None]]

    def write_roman(self,num):

        roman = OrderedDict()
        roman[1000] = "M"
        roman[900] = "CM"
        roman[500] = "D"
        roman[400] = "CD"
        roman[100] = "C"
        roman[90] = "XC"
        roman[50] = "L"
        roman[40] = "XL"
        roman[10] = "X"
        roman[9] = "IX"
        roman[5] = "V"
        roman[4] = "IV"
        roman[1] = "I"

        def roman_num(num):
            for r in roman.keys():
                x, y = divmod(num, r)
                yield roman[r] * x
                num -= (r * x)
                if num > 0:
                    roman_num(num)
                else:
                    break

        return "".join([a for a in roman_num(num)])
    
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
        file1 = open("Names/" + type[0] + ".txt", "r")
        file2 = open("Names/adjectives.txt", "r")
        file3 = open("Names/F.txt", "r")
        contents1 = file1.readlines()
        contents2 = file2.readlines()
        contents3 = file3.readlines()
        adjective = contents2
        name = contents3
        name2 = contents1
        WeaponName = "" 
        if(self.val <= 59): 
            full_name = random.choice(adjective)+" "+random.choice(name)
            WeaponName = full_name
        else:
            if(type[0] == "M" and self.val <= 80):
                full_name2 = "Book " + random.choice([self.write_roman(random.randint(0,14)), self.write_roman(random.randint(0,667))]) + ": " + random.choice(name2)
                WeaponName = full_name2
            else:
                full_name2 = random.choice(name2)
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

    def generate(self,type=[None]):
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
        if(type[0]==None):
            self.Weapon[0] = self.WeaponName(self.Weapon[1][4])
        else:
            self.Weapon[0] = self.WeaponName(type[0])
            self.Weapon[1][4] = type
        return self.Weapon