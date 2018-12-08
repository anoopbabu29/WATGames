from Multiplayer import MultiplayerConnection
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

connection = MultiplayerConnection()

roomName = input("Enter Room Name: ")
playerName = input("Enter Player Name: ")
roomSizeStr = input("Enter Room Size: ")
roomSize = 0
while(not roomSizeStr.isdigit() or int(roomSizeStr) > 10 or int(roomSizeStr) < 0):
    roomSizeStr = input("Enter Room Size Again: ")
roomSize = int(roomSizeStr)

results = connection.start(roomName,playerName,roomSize)
while(results == -1):
    roomName = input("Enter Room Name Again: ")
    results = connection.start(roomName,playerName,roomSize)

while(True):
    connection.waitTurn(roomName,1)
    print("Room " + roomName)
    print()
    connection.roomShow(roomName)
    print()
    print(connection.getGame(roomName))
    data = input("Write Something: ")
    print(connection.pushGame(roomName,data))
    connection.passTurn(roomName,2)