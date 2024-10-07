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
    return jsonify({
        "message" : "HOME"
    }), 200

@app.route("/redirect")
def redundantRedirect():
    # Specifically for OAuth on server-side Spotify requests
    return jsonify({
        "message" : "Redirect endpoint"
    }), 200

@app.route("/nextSong/<int:partyID>", methods=["GET"])
def nextSong(partyID: int):
    # Implement your logic here
    return jsonify({
        "message" : "Next song for party {partyID}"
    }), 200

@app.route("/queue/<int:partyID>", methods=["GET"])
def queue(partyID: int):
    # # Takes 3 songs from internal queue
    # partyID = probabilityDistro().keys()
    # return f"Queue for party {partyID[:3]}"
    
    return jsonify({
        "message" : "testing"
    }), 200

#linear search sucks :<
@app.route("/testEventCode/<string:eventCode>", methods=["GET"])
def testEventCode(eventCode: str):
    for event in DB.grabCollection("Event").stream:
        if event.eventCode == eventCode:
            return jsonify({
                "eventCodeFound" : "true"
            }), 200
    
    return jsonify({
        "eventCodeFound" : "false"
    }), 200

# Direct database interactions

#*****QUERY*****#

@app.route("/event/<str:eventID>", methods=["GET"])
def queryEvent(eventID: str):
    return jsonify(DB.getEventParams(eventID)), 200
    
@app.route("/user/<str:userID>", methods=["GET"])
def queryUser(userID: str):
    return jsonify(DB.getUserParams(userID)), 200

@app.route("/song/<str:songID>", methods=["GET"])
def querySong(songID: str):
    return jsonify(DB.getSongParams(songID)), 200

@app.route("/reaction/<str:reactionID>", methods=["GET"])
def queryReaction(reactionID: str):
    return jsonify(DB.getReactionParams(reactionID)), 200

#*****CREATE*****#
#all create funcs return ID of new stuff

@app.route("/user/create", methods=["POST", "OPTIONS"])
def createUser():
    if request.method == "OPTIONS":        
        return ""
    
    userData = request.get_json()
    id = DB.createUser(userData)
    if id:
        return jsonify({
            "id" : id
        }), 200
    else:
        return jsonify({
            "message" : "ERR creating user"
        }), 400

@app.route("/event/create", methods=["POST", "OPTIONS"])
def createEvent():
    if request.method == "OPTIONS":
        return ''
    
    eventData = request.get_json()
    id = DB.createUser(eventData)
    if id:
        return jsonify({
            "id" : id
        }), 200
    else:
        return jsonify({
            "message" : "ERR creating event"
        }), 400

@app.route("/song/create", methods=["POST", "OPTIONS"])
def createSong():
    if request.method == "OPTIONS":
        return ''
    
    songData = request.get_json()
    id = DB.createUser(songData)
    if id:
        return jsonify({
            "id" : id
        }), 200
    else:
        return jsonify({
            "message" : "ERR creating song"
        }), 200

@app.route("/reaction/create", methods=["POST", "OPTIONS"])
def createReaction():
    if request.method == "OPTIONS":
        return ''
    
    reactionData = request.get_json()
    id = DB.createUser(reactionData)
    if id:
        return jsonify({
            "id" : id
        }), 200
    else:
        return jsonify({
            "message" : "ERR creating reaction"
        }), 200

#*****DELETE*****#

@app.route("/user/delete", methods=["POST", "OPTIONS"])
def deleteUser():
    if request.method == "OPTIONS":
        return ''
    
    userData = request.get_json()
    rval = DB.deleteUser(userData)
    if rval:
        return jsonify({
            "message" : f"successful deletion of user ({userData})"
            }), 200
    else:
        return jsonify({
            "message" : "error, user not found"
        }), 400

@app.route("/event/delete", methods=["POST", "OPTIONS"])
def deleteEvent():
    if request.method == "OPTIONS":
        return ''
    eventData = request.get_json()
    rval = DB.deleteUser(eventData)
    if rval:
        return jsonify({
            "message" : f"successful deletion of event ({eventData})"
        }), 200
    else:
        return jsonify({
            "message" : "error, event not found"
        }), 400

@app.route("/song/delete", methods=["POST", "OPTIONS"])
def deleteSong():
    if request.method == "OPTIONS":
        return ''
    
    songData = request.get_json()
    rval = DB.deleteUser(songData)
    if rval:
        return jsonify({
            "message" : f"successful deletion of song ({songData})"
        }), 200
    else:
        return jsonify({
            "message": "error, song not found"
        }), 400

@app.route("/reaction/delete", methods=["POST", "OPTIONS"])
def deleteReaction():
    if request.method == "OPTIONS":
        return ''
    
    reactionData = request.get_json()
    rval = DB.deleteUser(reactionData)
    if rval:
        return jsonify({
            "message" : "success"
        }), 200
    else:
        return jsonify({
            "message" : "error, reaction not found"
        }), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)