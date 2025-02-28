import google.generativeai as genai

# 🔑 Din API-nyckel (se till att den är korrekt lagrad i miljövariabler)
API_KEY = "DIN_API_NYCKEL"

# 🔧 Konfigurera Google Gemini API
genai.configure(api_key="AIzaSyB6YnG_T5Gtkr7kEzHcWtw6rPcP7mdeTIg")

# 📌 Använd en giltig modell
model = genai.GenerativeModel("gemini-2.0-flash")  # Ändra till "gemini-2.0-flash" om du vill ha snabbare svar

# 🎤 Skicka en fråga till modellen
response = model.generate_content("Hej! Vad kan du göra?")

# 🖨️ Skriv ut svaret
print(response.text)