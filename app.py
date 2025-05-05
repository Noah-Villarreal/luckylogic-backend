from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import random
from collections import Counter
import os

app = Flask(__name__)
CORS(app)  # ✅ Allow React frontend to access backend

# ✅ Path to cleaned Powerball data
DATA_FILE = "src/data/CLEANED_Powerball_Numbers.csv"

# 🎯 Generate smart filtered Powerball picks
def generate_lucky_picks():
    print("🔁 Generating new Powerball picks...")

    df = pd.read_csv(DATA_FILE)
    for col in ['Num1', 'Num2', 'Num3', 'Num4', 'Num5', 'Powerball']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    main_numbers = pd.concat([df[f'Num{i}'] for i in range(1, 6)])
    powerball_numbers = df['Powerball']
    main_counts = Counter(main_numbers.dropna())
    powerball_counts = Counter(powerball_numbers.dropna())

    top_main = [n for n, _ in main_counts.most_common(20)]
    top_power = [n for n, _ in powerball_counts.most_common(10)]

    recent_nums = df.head(2)[['Num1', 'Num2', 'Num3', 'Num4', 'Num5']].values.flatten()
    top_main = [n for n in top_main if n not in recent_nums]

    picks = []
    while len(picks) < 5:
        pick = sorted(random.sample(top_main, 5))
        if not any(pick[i] - pick[i - 1] == 1 for i in range(1, 5)):
            power = random.choice(top_power)
            picks.append((pick, power))

    print("✅ Picks:", picks)
    return picks

# 🌐 Optional: Web route (not needed for API-only usage)
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", picks=None)

# 🌐 API route for frontend
@app.route("/api/pick", methods=["GET"])
def api_pick():
    picks = generate_lucky_picks()
    return jsonify({"picks": picks})

# 🚀 Run server (Render-compatible)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)

