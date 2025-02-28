import os
import google.generativeai as genai
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, request, jsonify

# Hämta API-nycklar
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

# Initiera Google Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Initiera Slack
client = WebClient(token=SLACK_BOT_TOKEN)
app = Flask(__name__)

# Funktion för att hämta svar från Gemini
def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip() if response.text else "Jag kunde inte förstå frågan."

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    print("🔍 Slack Event Data:", data)  # Logga inkommande data

    # Hantera Slacks Challenge-verifiering
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    # Hantera Slack-meddelanden
    if "event" in data:
        event = data["event"]

        if event.get("type") == "app_mention":  # När botten @-nämns
            user = event["user"]
            text = event["text"]
            channel = event["channel"]
            print(f"📩 Meddelande från @{user} i kanal {channel}: {text}")  # Logga inkommande meddelanden

            try:
                response_text = get_gemini_response(text)
                print(f"🤖 Gemini svar: {response_text}")  # Logga AI-svar

                client.chat_postMessage(channel=channel, text=f"🤖: {response_text}")
                print("✅ Meddelande skickat!")

            except SlackApiError as e:
                print(f"❌ Fel vid meddelandesändning: {e.response['error']}")

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)