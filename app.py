from flask import Flask, render_template, request
import random

app = Flask(__name__)

def simulate(cheat_mode):
    swag = booster = rare = tricky = 0
    score = 0

    for _ in range(1000):
        spin = random.randint(1, 100)

        if spin <= 40:
            swag += 1
            score += 2 if cheat_mode else 1
        elif spin <= 70:
            booster += 1
            score += 2
        elif spin <= 90:
            rare += 1
            score += 5
        else:
            tricky += 1
            score -= 1

    result = {
        "swag": swag,
        "booster": booster,
        "rare": rare,
        "tricky": tricky,
        "score": score
    }
    return result

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    mode = None
    compare = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "normal":
            result = simulate(False)
            mode = "Normal Mode"

        elif action == "cheat":
            result = simulate(True)
            mode = "Cheat Mode"

        elif action == "compare":
            normal = simulate(False)
            cheat = simulate(True)

            compare = {
                "normal": normal,
                "cheat": cheat,
                "verdict": "Cheat mode is WORTH it!" if cheat["score"] > normal["score"] else "Cheat mode is NOT worth it."
            }

    return render_template("index.html", result=result, mode=mode, compare=compare)

if __name__ == "__main__":
    app.run(debug=True)