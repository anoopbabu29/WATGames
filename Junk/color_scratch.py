class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Character():
    def __init__(self, Style, Weapon):
        self.Style = Style # S: Sword, A: Ax, L: Lance
        self.Weapon = Weapon

    def PrintCharacterDesign(self):
        print(bcolors.OKBLUE + "\u2588"*64 + bcolors.ENDC)
        for i in range(30):
            print("\u2588"*64)
        print("\u2588"*64)

c = Character("S","BladeOfTruth")
c.PrintCharacterDesign()