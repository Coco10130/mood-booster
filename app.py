from flask import Flask, jsonify
from flask_cors import CORS

import requests

app = Flask (__name__)
CORS(app)

@app.route("/")
def index() :
    return "This is flask"

@app.route("/api/cat-jokes", methods=["GET"])
def cat_jokes():
    try:
        response = requests.get('https://catfact.ninja/fact')
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/api/dog-pic", methods=["GET"])
def dog_pic():
    try:
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/jokes", methods=["GET"])
def random_jokes():
    try:
        response = requests.get('https://v2.jokeapi.dev/joke/Programming?type=twopart')
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)