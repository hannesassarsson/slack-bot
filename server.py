import os
import openai
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, request, jsonify

# Hämta tokens från miljövariabler
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initiera Slack och OpenAI
openai.api_key = OPENAI_API_KEY
client = WebClient(token=SLACK_BOT_TOKEN)
app = Flask(__name__)

# Funktion för att hantera meddelanden
def get_openai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    # 🛠 Hantera Slacks Challenge-request
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    # Hantera Slack-meddelanden
    if "event" in data:
        event = data["event"]

        if event.get("type") == "app_mention":  # När botten @-nämns
            user = event["user"]
            text = event["text"]
            channel = event["channel"]

            try:
                response_text = get_openai_response(text)
                client.chat_postMessage(channel=channel, text=f"🤖: {response_text}")

            except SlackApiError as e:
                print(f"Fel vid meddelandesändning: {e.response['error']}")

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)