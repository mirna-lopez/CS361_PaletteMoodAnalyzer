from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# Mood mapping based on color brightness and hue characteristics
MOOD_RULES = [
    {"name": "gothic",      "keywords": ["dark", "black", "crimson", "maroon", "deep"]},
    {"name": "whimsical",   "keywords": ["pink", "lavender", "mint", "pastel", "light"]},
    {"name": "romantic",    "keywords": ["rose", "blush", "coral", "peach", "warm"]},
    {"name": "noir",        "keywords": ["gray", "grey", "slate", "charcoal", "shadow"]},
    {"name": "fantasy",     "keywords": ["purple", "violet", "indigo", "gold", "azure"]},
    {"name": "serene",      "keywords": ["blue", "teal", "cyan", "sky", "ocean"]},
    {"name": "earthy",      "keywords": ["brown", "tan", "olive", "khaki", "sand"]},
    {"name": "energetic",   "keywords": ["red", "orange", "yellow", "lime", "bright"]},
    {"name": "mysterious",  "keywords": ["navy", "midnight", "dark blue", "deep purple"]},
    {"name": "natural",     "keywords": ["green", "forest", "sage", "moss", "jade"]},
]

HEX_PATTERN = re.compile(r'^#[0-9A-Fa-f]{6}$')

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def analyze_mood(hex_codes):
    moods = set()

    for hex_code in hex_codes:
        r, g, b = hex_to_rgb(hex_code)
        brightness = (r * 299 + g * 587 + b * 114) / 1000

        # Dark colors
        if brightness < 60:
            if r > g and r > b:
                moods.add("gothic")
            elif b > r and b > g:
                moods.add("mysterious")
            else:
                moods.add("noir")

        # Mid-range colors
        elif brightness < 150:
            if r > g and r > b:
                moods.add("romantic")
            elif g > r and g > b:
                moods.add("natural")
            elif b > r and b > g:
                moods.add("serene")
            elif r > 150 and g > 150:
                moods.add("earthy")
            else:
                moods.add("mysterious")

        # Bright/light colors
        else:
            if r > 200 and g < 100 and b < 100:
                moods.add("energetic")
            elif r > 200 and g > 150:
                moods.add("whimsical")
            elif b > 180 and r < 150:
                moods.add("serene")
            elif r > 180 and b > 180 and g < 150:
                moods.add("fantasy")
            else:
                moods.add("whimsical")

    return list(moods) if moods else ["neutral"]


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()

    if not data or 'colors' not in data:
        return jsonify({"error": "Request body must include a 'colors' key with an array of hex codes"}), 400

    colors = data['colors']

    if not isinstance(colors, list) or len(colors) < 1 or len(colors) > 10:
        return jsonify({"error": "colors must be an array of 1 to 10 hex codes"}), 400

    for color in colors:
        if not isinstance(color, str) or not HEX_PATTERN.match(color):
            return jsonify({"error": f"Invalid hex code: '{color}'. Expected format: #RRGGBB"}), 400

    moods = analyze_mood(colors)
    return jsonify({"moods": moods}), 200


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    app.run(port=5300, debug=True)