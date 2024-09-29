import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("github-actions@groove-437022.iam.gserviceaccount.com")
app = firebase_admin.initialize_app(cred)
cli = firestore.client()

def decompose(obj):
    return obj.to_dict().items()    

class DB:

    @staticmethod
    def getEventParams(eventID: str):
        for event in cli.collection("Event").stream():
            if event.id == eventID:
                return decompose(event)
        return {"Error" : "document not found"}

    @staticmethod
    def getUserParams(userID: str):
        for user in cli.collection("User").stream():
            if user.id == userID:
                return decompose(user)
        return {"Error" : "document not found"}

    @staticmethod
    def getSongParams(songID: str):
        for song in cli.collection("Song").stream():
            if song.id == songID:
                return decompose(song)
        return {"Error" : "document not found"}

    @staticmethod
    def getReactionParams(reactionID: str):
        for reaction in cli.collection("Reaction").stream():
            if reaction.id == reactionID:
                return decompose(reaction)
        return {"Error" : "document not found"}


    #setters & doc creation
    #TODO all
    @staticmethod
    def createEvent(eventData: dict):
        doc = cli.collection("Event").add(eventData) #returns new ID for eventDocument
        return doc.id
    
    @staticmethod
    def createUser(userData: dict):
        doc = cli.collection("User").add(userData) #returns new ID for eventDocument
        return doc.id

    @staticmethod
    def createSong(songData: dict):
        doc = cli.collection("Song").add(songData) #returns new ID for eventDocument
        return doc.id

    @staticmethod
    def createReaction(reactionData: dict):
        doc = cli.collection("Reaction").add(reactionData) #returns new ID for eventDocument
        return doc.id
    
    #deletions
    #TODO all

    @staticmethod
    def deleteEvent(eventID: int):
        for event in cli.collection("Event").stream():
            if event.id == eventID:
                event.delete()
        return {"Error" : "document not found"}
    
    @staticmethod
    def deleteUser(userID: int):
        for user in cli.collection("User").stream():
            if user.id == userID:
                user.delete()
        return {"Error" : "document not found"}

    @staticmethod
    def deleteSong(songID: int):
        for song in cli.collection("Song").stream():
            if song.id == songID:
                song.delete()
        return {"Error" : "document not found"}

    @staticmethod
    def deleteReaction(reactionID: int):
        for reaction in cli.collection("Reaction").stream():
            if reaction.id == reactionID:
                reaction.delete()
        return {"Error" : "document not found"}

