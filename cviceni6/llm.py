import google.generativeai as genai
from datetime import datetime
import sys
from abc import ABC, abstractmethod
from rag import WikiRAG, WeatherRAG, RateRAG



class LLM(ABC):
    def __init__(self, api_key, model_name='gemini-2.5-flash'):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.system_prompt = ''
    
    def set_system_prompt(self, prompt):
        self.system_prompt = prompt
    
    def generate_content(self, prompt):
        response = self.model.generate_content(self.system_prompt + prompt)
        return response.text


class TestLLM(LLM):
    def __init__(self, api_key, model_name='gemini-2.5-flash'):
        super().__init__(api_key, model_name)
        self.set_system_prompt("")


class ZemanLLM(LLM):
    def __init__(self, api_key, model_name='gemini-2.5-flash'):
        super().__init__(api_key, model_name)
        self.set_system_prompt("Odpovidej jako Milos Zeman, pri kazde odpovedi vyjadri, ze jsi chytrejsi nez tazatel")


class RagLLM(LLM):
    def __init__(self, api_key, model_name='gemini-2.5-flash'):
        super().__init__(api_key, model_name)
        self.set_system_prompt("""
Jsi asistent, ktery odpovida uzivateli na dotazy.
Pokud odpoved znas s jistotou, odpovez rovnou.
Pokud potrebujes dalsi informace, NEODPOVIDEJ - misto toho vrat POUZE jeden z nasledujicich radku:
- Pokud potrebujes vyhledat faktickou informaci nebo aktualni udalost (takovou o ktere si myslis, ze jeste nenastala): WIKI: <strucny dotaz vhodny pro vyhledavani>
- Pokud potrebujes informace o aktualnim pocasi: WEATHER: <zemepisna_sirka>,<zemepisna_delka>
- Pokud potrebujes aktualni kurz men: RATE: <KOD_MENY1>,<KOD_MENY2>,...
Zadny dalsi text nepridavej. Dotaz ve WIKI: radku pis cesky a co nejpresneji vystihni, co je treba vyhledat.
                               """)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python llm.py <PROMPT>")
        sys.exit(1)

    wiki = WikiRAG()
    weather = WeatherRAG()
    rates = RateRAG()

    prompt = sys.argv[1]

    while True:
        llm = RagLLM('YOUR_API_KEY')
        response = llm.generate_content(prompt)
        if response.startswith("WIKI:"):
            wiki_query = response[len("WIKI:"):].strip()
            wiki_result = wiki.retrieve(wiki_query)
            print(f"WIKI: {wiki_query}")
            prompt = f"\n\nDoplněné informace z Wikipedie:\n{wiki_result}\n\nOdpověz na původní dotaz: {prompt}"
        elif response.startswith("WEATHER:"):
            weather_query = response[len("WEATHER:"):].strip()
            weather_result = weather.retrieve(weather_query)
            print(f"WEATHER: {weather_query}")
            prompt = f"\n\nDoplněné informace o počasí:\n{weather_result}\n\nOdpověz na původní dotaz: {prompt}"
        elif response.startswith("RATE:"):
            rate_query = response[len("RATE:"):].strip()
            rate_result = rates.retrieve(rate_query)
            print(f"RATE: {rate_query}")
            prompt = f"\n\nDoplněné informace o kurzech:\n{rate_result}\n\nOdpověz na původní dotaz: {prompt}"
        else:
            break

    print(response)