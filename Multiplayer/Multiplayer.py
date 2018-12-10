import pyrebase
from PIL import Image
import json
import collections
import time
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Database():
    def __init__(self):
        config = {
            "apiKey": "AIzaSyCzpxiogj_Dsn6hGp2p69lMQ02eEIGc6rw",
            "authDomain": "hello-world-63cae.firebaseapp.com",
            "databaseURL": "https://hello-world-63cae.firebaseio.com",
            "storageBucket": "hello-world-63cae.appspot.com"
        }

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    # Pushes new data overwriting path data
    def push(self, path, data):
        return self.db.child(path).set(data)

    # Returns ordered dict of path
    def get(self, path):
        return self.db.child(path).get().val()

    # Appends new data to existing path
    def append(self, path, data):
        pathdata = self.get(path)
        for key, value in data.items():
            pathdata[key] = value
        self.push(path, pathdata)

    # Removes all data from a path
    def delete(self, path):
        self.db.child(path).remove()
        
    # Returns all data from database in an ordered dict
    def getAll(self):
        return self.db.child('').get().val() 
    
    # Used to print ordered dict
    def printOrderedDict(self,data,tab=0):
        if(type(data) != dict and type(data) != collections.OrderedDict):
            print("   " * tab + str(data))
        else:
            for key, value in data.items():
                print("   " * tab + str(key) + ":")
                self.printOrderedDict(value, tab + 1)

    # Prints all data from database
    def showAll(self):
        self.printOrderedDict(self.getAll())

    # Prints all data from database
    def show(self,path):
        self.printOrderedDict(self.get(path))

class MultiplayerConnection():
    def __init__(self):
        self.db = Database()
        self.isConnected = False
        self.updateTime = 1
        self.id = None
        self.dataChange = False

    def roomStatus(self,id):
        connections = True
        data = self.db.get("Multiplayer/" + str(id))
        for key, value in data.items():
            if("Player" in key and value == 'empty'):
                connections = False

        if(connections == True):
            self.isConnected = True

    def stream_handler(self,message):
        #print(message["event"]) # put
        #print(message["path"]) # /-K7yGTTEp7O549EzTYtI
        #print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
        self.dataChange = True
        

    def start(self,id,name,numPlayers = 2,game = None):
        connection = {
            id : {
                'Game' : "empty",
                'roomSize' : numPlayers,
                'Player 1': name,
                'Turn': 1
            }
        }

        for i in range(numPlayers-1):
            connection[id]['Player ' + str(i+2)] = 'empty'

        if(not (id in self.db.get("Multiplayer"))):
            self.db.append("Multiplayer", connection)
            if(game!=None):
                self.pushGame(id,game)
            timer = 120
            self.id = id
            self.my_stream = self.db.db.child("Multiplayer/" + str(id)).stream(self.stream_handler)
            while(not self.isConnected and timer >= 0):
                if self.dataChange:
                    clear()
                    print("Room: " + id + "\n")
                    self.db.show("Multiplayer/" + str(id))
                    print("Waiting For Friends...")
                    self.dataChange = False
                    self.roomStatus(self.id)
                time.sleep(self.updateTime)
                timer = timer - self.updateTime
                #self.roomStatus(id)
            if(self.isConnected):
                print("Room Full")
            else:
                print("No connection established")
        else:
            return -1

    def join(self,id,name):
        links = self.db.get("Multiplayer")
        for key, value in links.items():
            if(key == id):
                for key, value in value.items():
                    if("Player" in key and value != "empty"):
                        if(value ==  name):
                            return -2

                    if("Player" in key and value == "empty"):
                        self.db.push("Multiplayer/" + str(id) + "/" + key, name)
                        self.my_stream = self.db.db.child("Multiplayer/" + str(id)).stream(self.stream_handler)
                        return int(key.replace("Player ",""))
        return -1

    def getGame(self,id):
        return self.db.get("Multiplayer/" + str(id) + "/Game")

    def pushGame(self,id,data):
        return self.db.push("Multiplayer/" + str(id) + "/Game",data)

    def passTurn(self,id,new_position):
        return self.db.push("Multiplayer/" + str(id) + "/Turn",new_position)

    def waitTurn(self,id,position):
        while(int(self.db.get("Multiplayer/" + str(id) + "/Turn")) != position):
            if self.dataChange:
                #clear()
                #print("Room: " + id + "\n")
                print()
                #self.db.show("Multiplayer/" + str(id))
                print("Waiting for Player " + str(self.db.get("Multiplayer/" + str(id) + "/Turn")))
                self.dataChange = False

    def getTurn(self,id):
        return int(self.db.get("Multiplayer/" + str(id) + "/Turn"))

    def getRoomSize(self,id):
        return int(self.db.get("Multiplayer/" + str(id) + "/roomSize"))

    def roomShow(self,id):
        clear()
        self.db.show("Multiplayer/" + str(id))
    
    def close(self,id):
        clear()
        self.db.delete("Multiplayer/" + str(id))