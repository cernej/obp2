import google.generativeai as genai
import os

# API_KEY ziskate na https://aistudio.google.com/

genai.configure(api_key="API_KEY")

model = genai.GenerativeModel('gemini-2.5-flash')

prompt = "Jsi python programátor. Vytvoř jednoduchou ukázku použití genai a modelu gemini 3"

print("Čekám na odpověď od Gemini...")
response = model.generate_content(prompt)

print("\nOdpověď:")
print(response.text)