from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from markupsafe import escape

from database import DB

import requests
import os

from database import * # controller for document creation, retrieval, and editing

app = Flask(__name__)
CORS(app) #will accept any incoming traffic

@app.route("/")
@cross_origin
def home():
    return "HOME"

@app.route("/redirect")
@cross_origin
def redundantRedirect():
    # Specifically for OAuth on server-side Spotify requests
    return "Redirect endpoint"

@app.route("/nextSong/<int:partyID>", methods=["GET"])
@cross_origin
def nextSong(partyID: int):
    # Implement your logic here
    return f"Next song for party {partyID}"

@app.route("/queue/<int:partyID>", methods=["GET"])
@cross_origin
def queue(partyID: int):
    # # Takes 3 songs from internal queue
    # partyID = probabilityDistro().keys()
    # return f"Queue for party {partyID[:3]}"
    return "testing"

#linear search sucks :<
@app.route("/testEventCode/<string:eventCode>", methods=["GET"])
@cross_origin
def testEventCode(eventCode: str):
    for event in DB.grabCollection("Event").stream:
        if event.eventCode == eventCode:
            return {"eventCodeFound" : 1}
    return {"eventCodeFound" : 0}

# Direct database interactions

#*****QUERY*****#

@app.route("/event/<int:eventID>", methods=["GET"])
@cross_origin
def queryEvent(eventID: int):
    return DB.getEventParams(eventID)
    
@app.route("/user/<int:userID>", methods=["GET"])
@cross_origin
def queryUser(userID: int):
    return DB.getUserParams(userID)

@app.route("/song/<int:songID>", methods=["GET"])
@cross_origin
def querySong(songID: int):
    return DB.getSongParams(songID)

@app.route("/reaction/<int:reactionID>", methods=["GET"])
@cross_origin
def queryReaction(reactionID: int):
    return DB.getReactionParams(reactionID)

#*****CREATE*****#
#all create funcs return ID of new stuff

@app.route("/user/create", methods=["POST", "OPTIONS"])
@cross_origin
def createUser():
    if request.method == "OPTIONS":        
        return '', 200
    
    userData = request.get_json()
    id = DB.createUser(userData)
    if id:
        return {"id" : id}
    else:
        return "ERR, user not found"

@app.route("/event/create", methods=["POST", "OPTIONS"])
@cross_origin
def createEvent():
    if request.method == "OPTIONS":
        return '', 200
    
    eventData = request.get_json()
    id = DB.createUser(eventData)
    if id:
        return {"id" : id}
    else:
        return "ERR, event not found"

@app.route("/song/create", methods=["POST", "OPTIONS"])
@cross_origin
def createSong():
    if request.method == "OPTIONS":
        return '', 200
    
    songData = request.get_json()
    id = DB.createUser(songData)
    if id:
        return {"id" : id}
    else:
        return "ERR, song not found"

@app.route("/reaction/create", methods=["POST", "OPTIONS"])
@cross_origin
def createReaction():
    if request.method == "OPTIONS":
        return '', 200
    
    reactionData = request.get_json()
    id = DB.createUser(reactionData)
    if id:
        return {"id" : id}
    else:
        return "ERR, reaction not found"

#*****DELETE*****#

@app.route("/user/delete", methods=["POST", "OPTIONS"])
@cross_origin
def deleteUser():
    if request.method == "OPTIONS":
        return '', 200
    
    userData = request.get_json()
    rval = DB.deleteUser(userData)
    if rval:
        return {"success" : 100}
    else:
        return {"error, user not found" : 200}

@app.route("/event/delete", methods=["POST", "OPTIONS"])
@cross_origin
def deleteEvent():
    if request.method == "OPTIONS":
        return '', 200
    eventData = request.get_json()
    rval = DB.deleteUser(eventData)
    if rval:
        return {"success" : 100}
    else:
        return {"error, event not found" : 200}

@app.route("/song/delete", methods=["POST", "OPTIONS"])
@cross_origin
def deleteSong():
    if request.method == "OPTIONS":
        return '', 200
    
    songData = request.get_json()
    rval = DB.deleteUser(songData)
    if rval:
        return {"success" : 100}
    else:
        return {"error, song not found" : 200}

@app.route("/reaction/delete", methods=["POST", "OPTIONS"])
@cross_origin
def deleteReaction():
    if request.method == "OPTIONS":
        return '', 200
    
    reactionData = request.get_json()
    rval = DB.deleteUser(reactionData)
    if rval:
        return {"success" : 100}
    else:
        return {"error, reaction not found" : 200}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)