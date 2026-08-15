from flask import Flask, request, jsonify, send_from_directory
import re

app = Flask(__name__)


# -------------------------------
# Serve Frontend
# -------------------------------

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/style.css")
def css():
    return send_from_directory(".", "style.css")


@app.route("/script.js")
def javascript():
    return send_from_directory(".", "script.js")


# -------------------------------
# Scam Analysis API
# -------------------------------

@app.route("/api/analyze", methods=["POST"])
def analyze_call():

    data = request.get_json()

    transcript = data.get("transcript", "").lower()

    indicators = []
    score = 0

    # OTP / PIN
    if re.search(r"\botp\b|\bpin\b|password|verification code", transcript):
        indicators.append("OTP / PIN request detected")
        score += 25

    # Money
    if re.search(
        r"transfer money|send money|payment|bank account|upi|pay",
        transcript
    ):
        indicators.append("Money transfer request detected")
        score += 25

    # Urgency
    if re.search(
        r"urgent|immediately|right now|emergency|quickly|hurry",
        transcript
    ):
        indicators.append("Urgency / pressure detected")
        score += 20

    # Threat
    if re.search(
        r"blocked|police|arrest|legal action|account will be closed",
        transcript
    ):
        indicators.append("Threat / fear language detected")
        score += 15

    # Emotional manipulation
    if re.search(
        r"son|daughter|mother|father|family|accident|hospital",
        transcript
    ):
        indicators.append("Emotional manipulation detected")
        score += 15

    score = min(score, 100)

    if score >= 70:
        risk_level = "HIGH"
    elif score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return jsonify({
        "risk_score": score,
        "risk_level": risk_level,
        "voice_analysis": min(score + 3, 100),
        "nlp_analysis": score,
        "indicators": indicators
    })


# -------------------------------
# Start Backend Server
# -------------------------------

if __name__ == "__main__":

    print("--------------------------------")
    print("VOICE SCAM SHIELD BACKEND")
    print("Server starting...")
    print("--------------------------------")

    app.run(debug=True)