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
def home():
    return "HOME"

@app.route("/redirect")
def redundantRedirect():
    # Specifically for OAuth on server-side Spotify requests
    return "Redirect endpoint"

@app.route("/nextSong/<int:partyID>", methods=["GET"])
def nextSong(partyID: int):
    # Implement your logic here
    return f"Next song for party {partyID}"

@app.route("/queue/<int:partyID>", methods=["GET"])
def queue(partyID: int):
    # # Takes 3 songs from internal queue
    # partyID = probabilityDistro().keys()
    # return f"Queue for party {partyID[:3]}"
    pass
# Direct database interactions

#*****QUERY*****#

@app.route("/event/<int:eventID>", methods=["GET"])
def queryEvent(eventID: int):
    return DB.getEventParams(eventID)

@app.route("/user/<int:userID>", methods=["GET"])
def queryUser(userID: int):
    return DB.getUserParams(userID)

@app.route("/song/<int:songID>", methods=["GET"])
def querySong(songID: int):
    return DB.getSongParams(songID)

@app.route("/reaction/<int:reactionID>", methods=["GET"])
def queryReaction(reactionID: int):
    return DB.getReactionParams(reactionID)

#*****CREATE*****#

@app.route("/user/create", methods=["POST"])
def createUser():
    userData = request.get_json()
    return DB.createUser(userData)

@app.route("/event/create", methods=["POST"])
@cross_origin()
def createEvent():
    eventData = request.get_json()
    return DB.createEvent(eventData), 200

@app.route("/song/create", methods=["POST"])
def createSong():
    songData = request.get_json()
    return DB.createEvent(songData)

@app.route("/reaction/create", methods=["POST"])
def createReaction():
    reactionData = request.get_json()
    return DB.createEvent(reactionData)

#*****DELETE*****#

@app.route("/user/delete", methods=["POST"])
def deleteUser():
    userData = request.get_json()
    return DB.deleteUser(userData)

@app.route("/event/delete", methods=["POST"])
def deleteEvent():
    eventData = request.get_json()
    return DB.deleteEvent(eventData)

@app.route("/song/delete", methods=["POST"])
def deleteSong():
    songData = request.get_json()
    return DB.deleteEvent(songData)

@app.route("/reaction/delete", methods=["POST"])
def deleteReaction():
    reactionData = request.get_json()
    return DB.deleteEvent(reactionData)

if __name__ == "__main__":
    # For local development
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0/", port=port)
