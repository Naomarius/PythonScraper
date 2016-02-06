#!/usr/bin/env python
import requests
import xml.etree.ElementTree as ET

# URLs for retrieving from TheGamesDB API
GAMESDB_BASE  = "http://thegamesdb.net/api/"
PLATFORMLIST_URL = GAMESDB_BASE + "GetPlatformsList.php"
GAMEINFO_URL  = GAMESDB_BASE + "GetGame.php"
GAMESLIST_URL = GAMESDB_BASE + "GetPlatformGames.php"


def getPlatformID(str):
    id = "null"
    r = requests.get(PLATFORMLIST_URL)
    if r.status_code == 200:
        data = ET.fromstring(r.text.encode('ascii', 'ignore'))
        for platform in data.iter():
            #print(platform.tag, platform.attrib, platform.text)
            if platform.tag == 'id':
                id = platform.text
            if platform.tag == 'name':
                if platform.text == str:
                    break
    else:
        r.raise_for_status()

    return id

#
def getGame(platformID, gameName):
    gameInfo = []
    gameID = ""
    r = requests.get(GAMESLIST_URL, params={'platform': platformID})
    if r.status_code == 200:
        data = ET.fromstring(r.text.encode('ascii', 'ignore'))
        for game in data.iter():
            if game.tag == 'id':
                gameID = game.text
            if game.tag == 'GameTitle':
                if gameName in game.text:
                    gInfo = GameInfo(game.text, gameID)
                    gameInfo.append(gInfo)
                    #print(game.tag, game.attrib, game.text)
                    
            
    else:
        r.raise_for_status()
        
    return gameInfo

#
def getGameTest(platformID, gameName):
    r = requests.get(GAMESLIST_URL, params={'platform': platformID})
    if r.status_code == 200:
        data = ET.fromstring(r.text.encode('ascii', 'ignore'))
        for game in data.itertext():
            print(game, end='')
                    
            
    else:
        r.raise_for_status()

#
class GameInfo:
    def __init__(self, title, id):
        self.gameTitle = title
        self.gameID = id

    def displayInfo(self):
        print("GameTitle: " + self.gameTitle)
        print("GameID: " + self.gameID)

#main http://wiki.thegamesdb.net/index.php/API_Introduction
id = getPlatformID("Nintendo 64")
gameTitle = "F-Zero"

#getGameTest(platformID=id, gameName=gameTitle)

games = getGame(platformID=id, gameName=gameTitle)
print("===================================================================================")
print("64 PlatformID: " + id)
print("GameTitleSearched: " + gameTitle)
print("===================================================================================")
for game in games:
    game.displayInfo()
print("===================================================================================")
print("All done! Now refine the logic to handle parsing gametitles for possible matches!!!")

