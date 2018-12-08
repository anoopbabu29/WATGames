from Multiplayer import MultiplayerConnection
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

connection = MultiplayerConnection()

roomName = input("Enter Room Name: ")
playerName = input("Enter Player Name: ")

results = connection.join(roomName,playerName)
while(results < 0):
    if(results == -1):
        roomName = input("Enter Room Name Again: ")
    elif(results == -2):
        playerName = input("Enter Player Name Again: ")
    results = connection.join(roomName,playerName)

positon = results
roomSize = connection.getRoomSize(roomName)
connection.passTurn(roomName,(positon % roomSize) + 1)
while(True):
    connection.waitTurn(roomName,positon)
    print("Room " + roomName)
    print()
    connection.roomShow(roomName)
    print()
    print(connection.getGame(roomName))
    data = input("Write Something: ")
    print(connection.pushGame(roomName,data))
    connection.passTurn(roomName,(positon % roomSize) + 1)