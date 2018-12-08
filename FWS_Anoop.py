import os
import getpass

def isAlive(player, gameTokens):
    if(gameTokens[player] == None):
        return False

    for i in range(len(gameTokens[player])):
        if(gameTokens[player][i] < 0):
            return False   
    
    return True

def nextPlayer(player, gameTokens):
    nextPerson = (player + 1) % (len(gameTokens))
    while(not isAlive(nextPerson, gameTokens)):
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
    
    attackRes = getpass.getpass("\t\tPlayer " + str(attacker + 1) + "'s Attacking Resource (food: f, water: w, shelter: s): ")
    Roundout = Roundout + '\n\t\tPlayer ' + str(attacker + 1) + '\'s Attacking Resource (food: f, water: w, shelter: s): ' + attackRes
    
    attackResNum = FWSConverter(attackRes)
    while(attackResNum == 3):     
        attackRes = getpass.getpass("\t\tNot a valid resource. Attacking Resource (food: f, water: w, shelter: s): ")
        attackResNum = FWSConverter(attackRes)
        Roundout = Roundout + '\n\t\tNot a valid resource. Attacking Resource (food: f, water: w, shelter: s): ' + attackRes
   
    defendRes = getpass.getpass("\t\tPlayer " + str(defender + 1) + "'s Defending Resource (food: f, water: w, shelter: s): ")
    Roundout = Roundout + '\n\t\tPlayer ' + str(defender + 1) + '\'s Defending Resource (food: f, water: w, shelter: s): ' + defendRes
    
    defendResNum = FWSConverter(defendRes)
    while(defendResNum == 3):
        defendRes = getpass.getpass("\t\tNot a valid resource. Defending Resource (food: f, water: w, shelter: s): ")
        defendResNum = FWSConverter(defendRes)
        Roundout = Roundout + '\n\t\tNot a valid resource. Defending Resource (food: f, water: w, shelter: s): ' + defendRes
        
    
    if(attackResNum != defendResNum):
        Roundout = Roundout + '\n\t\tPlayer ' + str(attacker + 1) + ' sucessfully attacked'
        print("\t\tPlayer " + str(attacker + 1) + " sucessfully attacked")
        gameTokens[attacker][attackResNum] = gameTokens[attacker][attackResNum] + 1
        gameTokens[defender][attackResNum] = gameTokens[defender][attackResNum] - 1
    else:
        Roundout = Roundout + '\n\t\tPlayer ' + str(defender + 1) + ' successfully defended'
        print("\t\tPlayer " + str(defender + 1) + " successfully defended")
    gameTokens[defender][defendResNum] = gameTokens[defender][defendResNum] + 1
    
    return [gameTokens, Roundout]

def attackingTurn(currentPlayer, gameTokens, Roundout):
    if(gameTokens[currentPlayer] == None):
        return [gameTokens, Roundout]
    else:
        Roundout = Roundout + '\n\tPlayer ' + str(currentPlayer + 1) + '\'s turn:'
        print('\tPlayer ' + str(currentPlayer + 1) + '\'s turn:')
        defendingPlayer = int(input("\t\tWhich player do you want to attack? ")) - 1
        Roundout = Roundout + "\n\t\tWhich player do you want to attack? " + str(defendingPlayer)
        while((defendingPlayer >= numPlayers or defendingPlayer < 0) or gameTokens[defendingPlayer] == None or currentPlayer == defendingPlayer):
            defendingPlayer = int(input("\t\tThat player is not in this game. Please pick another player: ")) - 1
            Roundout = Roundout + '\n\t\tThat player is not in this game. Please pick another player: ' + str(defendingPlayer)
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
    print('Status:')
    for i in range(len(gameTokens)):
        if(not isAlive(i, gameTokens)):
            print('Player ' + str(i + 1) + ':  Dead')
        else:
            print('Player ' + str(i + 1) + ':  Food: ' + str(gameTokens[i][0]) + '  Water: ' + str(gameTokens[i][1]) + '  Shelter: ' + str(gameTokens[i][2]))
    print(' ')

if __name__ == "__main__":
    isWinner = False
    roundNum = 1
    currentPlayer = 0

    numPlayers = int(input("Enter the number of people playing FWS: "))

    gameTokens = [None] * numPlayers

    for i in range(numPlayers):
        gameTokens[i] = [3, 3, 3]

    os.system('cls' if os.name == 'nt' else 'clear')
    printStatus(gameTokens)

    while(not isWinner):
        Roundout = 'Round #' + str(roundNum) + ': '       
        print(Roundout)
        
        count = 0
        startingPlayer = currentPlayer 

        #Everyone is attacking in the round

        #Do-While loop
        gameTokens, Roundout = attackingTurn(currentPlayer, gameTokens, Roundout)
        currentPlayer = nextPlayer(currentPlayer, gameTokens)
        os.system('cls' if os.name == 'nt' else 'clear')
        printStatus(gameTokens)
        print(Roundout)
        while(currentPlayer != startingPlayer): #Possible Bug: If the starting Player loses, it will be an infinite loop
            gameTokens, Roundout = attackingTurn(currentPlayer, gameTokens, Roundout)
            currentPlayer = nextPlayer(currentPlayer, gameTokens)
            os.system('cls' if os.name == 'nt' else 'clear')
            printStatus(gameTokens)
            print(Roundout)
        
        print('')
        #Starting Player gets to choose the resource to lower
            #Needs to prevent player from being able to self-destruct
        loweredRes = input("\tPlayer " + str(currentPlayer + 1) + ", which resource would you like to lower (food: f, water: w, shelter: s)? ")
        
        loweredResNum = FWSConverter(loweredRes)
        while(loweredResNum == 3):
            loweredResNum = FWSConverter(input("\tNot a valid resource. Which resource would you like to lower (food: f, water: w, shelter: s)? "))
        
        
        gameTokens, count = lowerRes(loweredResNum,gameTokens)
        
        currentPlayer = nextPlayer(currentPlayer, gameTokens)
        roundNum = roundNum + 1

        if(count == 1):
            currrentPlayer = findWinner(gameTokens)
            isWinner = True
        if(count == 0):
            currentPlayer = -1
            isWinner = True

        os.system('cls' if os.name == 'nt' else 'clear')
        printStatus(gameTokens)

    if(currentPlayer != -1):
        print('Winner: Player ' + str(currentPlayer + 1))
    else:
        print('Draw!')