from flask import Flask
from markupsafe import escape


import jsonify, requests


app = Flask(__name__)

@app.route("/redirect")
def redundantRedirect():
    #specifically for oauth on serverside spotify requests
    return

@app.route("/nextSong/int:<partyID>", methods=["GET"])
def nextSong():
    pass

@app.route("/queue/<int:partyID>", methods=["GET"])
def queue():
    #takes a 3 songs from internal queue
    pass

#direct database interactions

@app.route("/party/int:<partyID>", methods=["GET"])
def queryParty():
    pass