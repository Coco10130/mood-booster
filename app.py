from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

favorites = []

@app.route("/")
def index():
    return render_template("index.html")

#! Cat Facts
@app.route("/api/cat/random", methods=["GET"])
def random_cat_facts():
    try:
        cat_facts = []
        # Fetch 3 random cat facts
        for _ in range(3):
            response = requests.get("https://catfact.ninja/fact")
            cat_facts.append(response.json())
        return jsonify(cat_facts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/cat/random/<int:length>", methods=["GET"])
def random_cat_facts_length(length):
    try:
        cat_facts = []
        for _ in range(3):
            url = f"https://catfact.ninja/fact?max_length={length}"
            response = requests.get(url)
            cat_facts.append(response.json())
        return jsonify(cat_facts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#! Random Dogs
@app.route("/api/dog/random", methods=["GET"])
def random_dog_images():
    try:
        dog_images = []
        # Fetch 3 random dog images
        for _ in range(3):
            response = requests.get("https://dog.ceo/api/breeds/image/random")
            dog_images.append(response.json())
        return jsonify(dog_images)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#! Random Jokes
@app.route("/api/joke/random", methods=["GET"])
def random_jokes():
    try:
        jokes = []
        for _ in range(3):
            response = requests.get("https://v2.jokeapi.dev/joke/Any")
            joke_data = response.json()
            if joke_data.get("type") == "twopart":
                joke = {
                    "type": "twopart",
                    "setup": joke_data.get("setup", ""),
                    "punchline": joke_data.get("delivery", "")
                }
            elif joke_data.get("type") == "single":
                joke = {
                    "type": "single",
                    "joke": joke_data.get("joke", "")
                }
            else:
                joke = {"error": "No joke found"}
            jokes.append(joke)
        return jsonify(jokes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/joke/random/<string:category>", methods=["GET"])
def random_jokes_by_category(category):
    try:
        jokes = []
        for _ in range(3):
            url = f"https://v2.jokeapi.dev/joke/{category}"
            response = requests.get(url)
            joke_data = response.json()

            if joke_data.get("type") == "twopart":
                joke = {
                    "type": "twopart",
                    "setup": joke_data.get("setup", ""),
                    "punchline": joke_data.get("delivery", "")
                }
            elif joke_data.get("type") == "single":
                joke = {
                    "type": "single",
                    "joke": joke_data.get("joke", "")
                }
            else:
                joke = {"error": "No joke found or invalid category"}
            
            jokes.append(joke)

        return jsonify(jokes)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/api/mood-booster", methods=["GET"])
def mood_booster():
    try:
        cat_facts = []
        dog_images = []
        jokes = []

        # Fetch 3 random cat facts
        for _ in range(3):
            cat_response = requests.get("https://catfact.ninja/fact")
            cat_facts.append(cat_response.json())

        # Fetch 3 random dog images
        for _ in range(3):
            dog_response = requests.get("https://dog.ceo/api/breeds/image/random")
            dog_images.append(dog_response.json())

        # Fetch 3 random jokes
        for _ in range(3):
            joke_response = requests.get("https://v2.jokeapi.dev/joke/Any")
            joke_data = joke_response.json()
            if joke_data.get("type") == "twopart":
                joke = {
                    "type": "twopart",
                    "setup": joke_data.get("setup", ""),
                    "punchline": joke_data.get("delivery", "")
                }
            elif joke_data.get("type") == "single":
                joke = {
                    "type": "single",
                    "joke": joke_data.get("joke", "")
                }
            else:
                joke = {"error": "No joke found"}
            jokes.append(joke)

        # Return a combined mood-booster with 3 items each
        return jsonify({
            "mood_booster": [
                {"type": "cat_fact", "content": [fact.get("fact") for fact in cat_facts]},
                {"type": "dog_image", "content": [image.get("message") for image in dog_images]},
                {"type": "joke", "content": jokes}
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/favorites", methods=["POST"])
def add_favorite():
    data = request.json
    if not data or "type" not in data or "content" not in data:
        return jsonify({"error": "Invalid data"}), 400

    favorites.append(data)
    return jsonify({"message": "Favorite added", "favorites": favorites}), 201

@app.route("/api/favorites", methods=["GET"])
def get_favorites():
    return jsonify({"favorites": favorites})

@app.route("/api/favorites/<string:type>", methods=["GET"])
def get_favorites_by_type(type):
    filtered = [fav for fav in favorites if fav["type"] == type]
    return jsonify({"favorites": filtered})

@app.route("/api/favorites/<int:index>", methods=["DELETE"])
def delete_favorite(index):
    if 0 <= index < len(favorites):
        removed = favorites.pop(index)
        return jsonify({"message": "Favorite removed", "removed": removed})
    return jsonify({"error": "Index out of range"}), 404

@app.route("/api/favorites/clear", methods=["DELETE"])
def clear_favorites():
    favorites.clear()
    return jsonify({"message": "All favorites cleared"})

if __name__ == "__main__":
    app.run(debug=True)