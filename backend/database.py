import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

firebase_admin.initialize_app()
cli = firestore.client()

def decompose(obj):
    return obj.to_dict()    

class DB:

    @staticmethod
    def getEventParams(eventID: str):
        eventDoc = cli.collection("Event").document(eventID).get()
        if eventDoc.exists:
            return decompose(eventDoc)
        return {"Error" : f"{eventID} not found"}

    @staticmethod
    def getUserParams(userID: str):
        userDoc = cli.collection("User").document(userID).get()
        if userDoc.exists:
            return decompose(userDoc)
        return {"Error" : f"{userID} not found"}

    @staticmethod
    def getSongParams(songID: str):
        songDoc = cli.collection("Song").document(songID).get()
        if songDoc.exists:
            return decompose(songDoc)
        return {"Error" : f"{songID} not found"}

    @staticmethod
    def getReactionParams(reactionID: str):
        reactionDoc = cli.collection("Reaction").document(reactionID).get()
        if reactionDoc.exists:
            return decompose(reactionDoc)
        return {"Error" : f"{reactionID} not found"}

    @staticmethod
    def getUserSongParams(userSongID: str):
        userSongDoc = cli.collection("UserSong").document(userSongID).get()
        if userSongDoc.exists:
            return decompose(userSongDoc)
        return {"Error" : f"{userSongID} not found"}

    #setters & doc creation

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
    
    @staticmethod
    def createUserSong(userSongData: dict):
        doc = cli.collection("UserSong").add(userSongData) #returns new ID for eventDocument
        return doc.id
    
    #deletions

    @staticmethod
    def deleteEvent(eventID: str):
        eventRef = cli.collection("Event").document(eventID)
        eventDoc = eventRef.get()
        if eventDoc.exists:
            eventRef.delete()
            return {"message" : "successful deletion"}
        return {"Error" : f"{eventID} not found"}

    @staticmethod
    def deleteUser(userID: str):
        userRef = cli.collection("User").document(userID)
        userDoc = userRef.get()
        if userDoc.exists:
            userRef.delete()
            return {"message" : "successful deletion"}
        return {"Error" : f"{userID} not found"}

    @staticmethod
    def deleteSong(songID: str):
        songRef = cli.collection("Song").document(songID)
        songDoc = songRef.get()
        if songDoc.exists:
            songRef.delete()
            return {"message" : "successful deletion"}
        return {"Error" : f"{songID} not found"}

    @staticmethod
    def deleteReaction(reactionID: str):
        reactionRef = cli.collection("Reaction").document(reactionID)
        reactionDoc = reactionRef.get()
        if reactionDoc.exists:
            reactionRef.delete()
            return {"message" : "successful deletion"}
        return {"Error" : f"{reactionID} not found"}

    @staticmethod
    def deleteSong(userSongID: str):
        userSongRef = cli.collection("UserSong").document(userSongID)
        userSongDoc = userSongRef.get()
        if userSongDoc.exists:
            userSongRef.delete()
            return {"message" : "successful deletion"}
        return {"Error" : f"{userSongID} not found"}

    @staticmethod
    def grabCollection(collectionName: str):
        """
        serverside use only
        """
        return cli.collection(collectionName)