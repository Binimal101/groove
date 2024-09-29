from flask import Flask, jsonify
from markupsafe import escape
import requests
import os

app = Flask(__name__)

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
    # Takes 3 songs from internal queue
    return f"Queue for party {partyID}"

# Direct database interactions
@app.route("/party/<int:partyID>", methods=["GET"])
def queryParty(partyID: int):
    # Implement your logic here
    return f"Party details for {partyID}"

if __name__ == "__main__":
    # For local development
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0/", port=port)
