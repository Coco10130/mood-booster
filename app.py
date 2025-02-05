from flask import Flask, jsonify
import requests

app = Flask (__name__)

@app.route("/")
def index():
    try:
        response = requests.get('https://catfact.ninja/fact')
        data = response.json()
        return jsonify(data)  # Returning the cat fact as JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)