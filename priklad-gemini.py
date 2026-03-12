import google.generativeai as genai
import os

# 1. Konfigurace API klíče
# Doporučená metoda (pokud si nastavíte systémovou proměnnou):
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Pro rychlý test (nahraďte VÁŠ_API_KLÍČ svým skutečným klíčem):
genai.configure(api_key="VÁŠ_API_KLÍČ")

# 2. Inicializace modelu
# Model 'gemini-1.5-flash' je aktuálně nejlepší volba pro rychlé a obecné úkoly
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. Příprava dotazu (promptu)
prompt = "Jsi python programátor. Napiš mi jednoduchou funkci, která vypíše 'Ahoj světe!'"

# 4. Získání a vypsání odpovědi
print("Čekám na odpověď od Gemini...")
response = model.generate_content(prompt)

print("\nOdpověď:")
print(response.text)