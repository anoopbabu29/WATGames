import os
import getpass

def isAlive(player, gameTokens):
    if(gameTokens[player] == None):
        return False

    for i in range(len(gameTokens[player])):
        if(gameTokens[player][i] < 0):
            return False   
    
    return True

def nextPlayer(player, stopPlayer, gameTokens):
    nextPerson = (player + 1) % (len(gameTokens))
    while((not isAlive(nextPerson, gameTokens)) and (nextPerson != stopPlayer)):
        nextPerson = (nextPerson + 1) % (len(gameTokens))

    return nextPerson

def FWSConverter(res):
    num = 3
    if(res.lower() == "f"):
        num = 0
    elif(res.lower() == "w"):
        num = 1
    elif(res.lower() == "s"):
        num = 2
    
    return num

def attack(attacker, defender, gameTokens, Roundout):
    #function for attacking someone
    
    attackRes = getpass.getpass("\t\t\33[0mPlayer " + str(attacker + 1) + "'s Attacking Resource (food: f, water: w, shelter: s): \033[0m")
    Roundout = Roundout + '\n\t\t\33[0mPlayer ' + str(attacker + 1) + '\'s Attacking Resource (food: f, water: w, shelter: s): \033[0m' + attackRes
    
    attackResNum = FWSConverter(attackRes)
    while(attackResNum == 3):     
        attackRes = getpass.getpass("\t\t\33[0mNot a valid resource. Attacking Resource (food: f, water: w, shelter: s): \033[0m")
        attackResNum = FWSConverter(attackRes)
        Roundout = Roundout + '\n\t\t\33[0mNot a valid resource. Attacking Resource (food: f, water: w, shelter: s): \033[0m' + attackRes
   
    defendRes = getpass.getpass("\t\t\33[0mPlayer " + str(defender + 1) + "'s Defending Resource (food: f, water: w, shelter: s): \033[0m")
    Roundout = Roundout + '\n\t\t\33[0mPlayer ' + str(defender + 1) + '\'s Defending Resource (food: f, water: w, shelter: s): \033[0m' + defendRes
    
    defendResNum = FWSConverter(defendRes)
    while(defendResNum == 3):
        defendRes = getpass.getpass("\t\t\33[0mNot a valid resource. Defending Resource (food: f, water: w, shelter: s): \033[0m")
        defendResNum = FWSConverter(defendRes)
        Roundout = Roundout + '\n\t\t\33[0mNot a valid resource. Defending Resource (food: f, water: w, shelter: s): \033[0m' + defendRes
        
    
    if(attackResNum != defendResNum):
        Roundout = Roundout + '\n\t\t\33[0mPlayer ' + str(attacker + 1) + ' sucessfully attacked\033[0m'
        print("\t\t\33[0mPlayer " + str(attacker + 1) + " sucessfully attacked\033[0m")
        gameTokens[attacker][attackResNum] = gameTokens[attacker][attackResNum] + 1
        gameTokens[defender][attackResNum] = gameTokens[defender][attackResNum] - 1
    else:
        Roundout = Roundout + '\n\t\t\33[0mPlayer ' + str(defender + 1) + ' successfully defended\033[0m'
        print("\t\t\33[0mPlayer " + str(defender + 1) + " successfully defended\033[0m")
    gameTokens[defender][defendResNum] = gameTokens[defender][defendResNum] + 1
    
    return [gameTokens, Roundout]

def attackingTurn(currentPlayer, gameTokens, Roundout):
    if(gameTokens[currentPlayer] == None):
        return [gameTokens, Roundout]
    else:
        Roundout = Roundout + '\n\t\33[35mPlayer ' + str(currentPlayer + 1) + '\'s turn:\033[0m'
        print('\t\33[35mPlayer ' + str(currentPlayer + 1) + '\'s turn:\033[0m')
        defendingPlayerStr = input("\t\t\33[0mWhich player do you want to attack? \033[0m")
        Roundout = Roundout + "\n\t\t\33[0mWhich player do you want to attack? \033[0m" + defendingPlayerStr
        while(not defendingPlayerStr.isdigit()):
            defendingPlayerStr = input("\t\t\33[0mThat is not a valid input. Which player do you want to attack? \033[0m")
            Roundout = Roundout + "\n\t\t\33[0mThat is not a valid input. Which player do you want to attack? \033[0m" + defendingPlayerStr
        defendingPlayer = int(defendingPlayerStr) - 1

        
        while((defendingPlayer >= numPlayers or defendingPlayer < 0) or gameTokens[defendingPlayer] == None or currentPlayer == defendingPlayer):
            defendingPlayerStr = input("\t\t\33[0mThat is not a valid input. Which player do you want to attack? \033[0m")
            Roundout = Roundout + "\n\t\t\33[0mThat is not a valid input. Which player do you want to attack? \033[0m" + defendingPlayerStr
            while(not defendingPlayerStr.isdigit()):
                defendingPlayerStr = input("\t\t\33[0mThat is not a valid input. Which player do you want to attack? \033[0m")
                Roundout = Roundout + "\n\t\t\33[0mThat is not a valid input. Which player do you want to attack? \033[0m" + defendingPlayerStr
            defendingPlayer = int(defendingPlayerStr) - 1
        gameTokens, Roundout = attack(currentPlayer, defendingPlayer, gameTokens, Roundout)
        
        if(not isAlive(defendingPlayer, gameTokens)):
            gameTokens[defendingPlayer] = None
    
    return [gameTokens, Roundout]

def lowerRes(res, gameTokens):
    count = 0
    
    for i in range(len(gameTokens)):
        if(gameTokens[i] == None):
            continue
        else:
            if(res != -1):
                gameTokens[i][res] = gameTokens[i][res] - 2
            if(not isAlive(i, gameTokens)):
                gameTokens[i] = None
            else:
                count = count + 1
    
    return gameTokens, count

def findWinner(gameTokens):
    for i in range(len(gameTokens)):
        if(gameTokens[i] != None):
            return i
    
    return -1

def printStatus(gameTokens):
    print('\33[33mStatus:\033[0m')
    for i in range(len(gameTokens)):
        if(not isAlive(i, gameTokens)):
            print('\33[35mPlayer ' + str(i + 1) + ':\033[0m' + '  \33[31mDead\033[0m')
        else:
            print('\33[35mPlayer ' + str(i + 1) + ':\033[0m'+'  \33[32mFood: \033[0m' + str(gameTokens[i][0]) + '  \33[96mWater: \033[0m' + str(gameTokens[i][1]) + '  \33[94mShelter: \033[0m' + str(gameTokens[i][2]))
    print(' ')

if __name__ == "__main__":
    isWinner = False
    roundNum = 1
    currentPlayer = 0

    
    numPlayersStr = input("Enter the number of people playing FWS: ")
    while(not numPlayersStr.isdigit()):
        numPlayersStr = input("That is not a valid input. Enter the number of people playing FWS: ")

    numPlayers = int(numPlayersStr)

    gameTokens = [None] * numPlayers

    for i in range(numPlayers):
        gameTokens[i] = [3, 3, 3]

    os.system('cls' if os.name == 'nt' else 'clear')
    printStatus(gameTokens)

    while(not isWinner):
        Roundout = '\33[33mRound #' + str(roundNum) + ': \033[0m'       
        print(Roundout)
        
        count = 0
        startingPlayer = currentPlayer 

        #Everyone is attacking in the round

        #Do-While loop
        gameTokens, Roundout = attackingTurn(currentPlayer, gameTokens, Roundout)
        currentPlayer = nextPlayer(currentPlayer, startingPlayer, gameTokens)
        os.system('cls' if os.name == 'nt' else 'clear')
        printStatus(gameTokens)
        print(Roundout)
        while(currentPlayer != startingPlayer): #Possible Bug: If the starting Player loses, it will be an infinite loop
            gameTokens, Roundout = attackingTurn(currentPlayer, gameTokens, Roundout)
            currentPlayer = nextPlayer(currentPlayer, startingPlayer, gameTokens)
            os.system('cls' if os.name == 'nt' else 'clear')
            printStatus(gameTokens)
            print(Roundout)
        
        print('')
        #Starting Player gets to choose the resource to lower
            #Needs to prevent player from being able to self-destruct
        lowerResNum = -1
        if(isAlive(currentPlayer, gameTokens)):
            loweredRes = input("\tPlayer " + str(currentPlayer + 1) + ", which resource would you like to lower (food: f, water: w, shelter: s)? ")
            loweredResNum = FWSConverter(loweredRes)
            while(loweredResNum == 3):
                loweredResNum = FWSConverter(input("\tNot a valid resource. Which resource would you like to lower (food: f, water: w, shelter: s)? "))

        gameTokens, count = lowerRes(loweredResNum,gameTokens)

        os.system('cls' if os.name == 'nt' else 'clear')
        printStatus(gameTokens)
        
        if(count == 1):
            currrentPlayer = findWinner(gameTokens)
            isWinner = True
            break
        if(count == 0):
            currentPlayer = -1
            isWinner = True
            break
        
        currentPlayer = nextPlayer(currentPlayer, -1, gameTokens)
        roundNum = roundNum + 1

    for i in range(len(gameTokens)):
        if(gameTokens[i] == None):
            continue
        else:
            currentPlayer = i
            break

    if(currentPlayer != -1):
        print('Winner: Player ' + str(currentPlayer + 1))
    else:
        print('Draw!')