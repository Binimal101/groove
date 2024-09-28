from flask import Flask
import jsonify, requests

app = Flask(__name__)

@app.route("/nextSong", methods=["GET"])
def nextSong():
    pass

@app.route("/queue", methods=["POST"])
def queue():
    #takes a number N from post request