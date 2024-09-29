from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#getters
class DB:
    mongoPass="ML8w@VN_bsRu!@M"
    uri = "mongodb+srv://matthewtujague:{mongoPass}@groove.11ipv.mongodb.net/?retryWrites=true&w=majority&appName=groove"
    global client
    client = MongoClient(uri, server_api=ServerApi('1'))["grooveDB"]

    @staticmethod
    def getEventParams(eventID: str):
        pass

    @staticmethod
    def getUserParams(userID: str):
        pass

    @staticmethod
    def getSongParams(songID: str):
        pass

    @staticmethod
    def getReactionParams(reactionID: str):
        pass


    #setters & doc creation
    #TODO all
    @staticmethod
    def createEvent(eventData: dict):
        event_collection = client['Event']
        result = event_collection.insert_one(eventData) #returns new ID for eventDocument
        return result
    
    @staticmethod
    def createUser(userData: dict):
        event_collection = client['User']
        result = event_collection.insert_one(userData) #returns new ID for eventDocument
        return result

    @staticmethod
    def createSong(songData: dict):
        event_collection = client['Song']
        result = event_collection.insert_one(songData) #returns new ID for eventDocument
        return result

    @staticmethod
    def createReaction(reactionData: dict):
        event_collection = client['Reaction']
        result = event_collection.insert_one(reactionData) #returns new ID for eventDocument
        return result
    
    #deletions
    #TODO all

    @staticmethod
    def deleteEvent(eventID: int):
        event_collection = client['Event']
        result = event_collection.insert_one(eventID) #returns new ID for eventDocument
        return result
    
    @staticmethod
    def deleteUser(userID: int):
        event_collection = client['User']
        result = event_collection.insert_one(userID) #returns new ID for eventDocument
        return result

    @staticmethod
    def deleteSong(songID: int):
        event_collection = client['Song']
        result = event_collection.insert_one(songID) #returns new ID for eventDocument
        return result

    @staticmethod
    def deleteReaction(reactionID: int):
        event_collection = client['Reaction']
        result = event_collection.insert_one(reactionID) #returns new ID for eventDocument
        return result

