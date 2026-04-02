import google.generativeai as genai
from datetime import datetime
import sys
from abc import ABC, abstractmethod
from rag import KiwiRAG, WikiRAG, WeatherRAG, RateRAG



class LLM(ABC):
    def __init__(self, api_key, model_name='gemini-2.5-flash'):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.context = []
        self.system_prompt = ''
    
    def set_system_prompt(self, prompt):
        self.system_prompt = prompt
    
    def generate_content(self, prompt, context=None):
        self.context.append(prompt)
        context = "\n\nKontext nasi predchozi konverzace, pouzivej pouze, pokud nevis odpoved z predchozi casti textu: " + "\n".join(self.context) if context else ""
        dotaz = self.system_prompt + prompt + context
        print(f"LLM dotaz: {dotaz}")
        response = self.model.generate_content(dotaz)
        self.context.append(response.text)
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
        self.set_system_prompt(f"""
Dnes je {datetime.now().strftime('%Y-%m-%d')}.
Jsi asistent, ktery odpovida uzivateli na dotazy.
Pokud odpoved znas s jistotou, odpovez rovnou.
Pokud se ti zda, ze se uzivatel pta na veci, ktere jeste nenastaly nebo pokud potrebujes dalsi informace, NEODPOVIDEJ - misto toho vrat POUZE jeden z nasledujicich radku:
- Pokud potrebujes vyhledat faktickou informaci nebo aktualni udalost (takovou o ktere si myslis, ze jeste nenastala): WIKI: <strucny dotaz vhodny pro vyhledavani>
- Pokud potrebujes informace o aktualnim pocasi: WEATHER: <zemepisna_sirka>,<zemepisna_delka>
- Pokud potrebujes aktualni kurz men: RATE: <KOD_MENY1>,<KOD_MENY2>,...
- Pokud potrebujes vyhledat lety pres Kiwi API: KIWI: <odkud>,<kam>,<kdy>
Zadny dalsi text nepridavej. Dotaz ve WIKI: radku pis cesky a co nejpresneji vystihni, co je treba vyhledat.
                               """)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python llm.py <PROMPT>")
        sys.exit(1)

    wiki = WikiRAG()
    weather = WeatherRAG()
    rates = RateRAG()
    kiwi = KiwiRAG('VAS_KIWI_API_KLIC')

    prompt = sys.argv[1]

    while True:
        llm = RagLLM('VAS_API_KLIC')
        response = llm.generate_content(prompt)
        if response.startswith("WIKI:"):
            wiki_query = response[len("WIKI:"):].strip()
            print(f"WIKI: {wiki_query}")
            wiki_result = wiki.retrieve(wiki_query)
            prompt = f"\n\nDoplněné informace z Wikipedie:\n{wiki_result}\n\nOdpověz na původní dotaz: {prompt}"
        elif response.startswith("WEATHER:"):
            weather_query = response[len("WEATHER:"):].strip()
            print(f"WEATHER: {weather_query}")
            weather_result = weather.retrieve(weather_query)
            prompt = f"\n\nDoplněné informace o počasí:\n{weather_result}\n\nOdpověz na původní dotaz: {prompt}"
        elif response.startswith("RATE:"):
            rate_query = response[len("RATE:"):].strip()
            print(f"RATE: {rate_query}")
            rate_result = rates.retrieve(rate_query)
            prompt = f"\n\nDoplněné informace o kurzech:\n{rate_result}\n\nOdpověz na původní dotaz: {prompt}"
        elif response.startswith("KIWI:"):
            kiwi_query = response[len("KIWI:"):].strip()
            print(f"KIWI: {kiwi_query}")
            kiwi_result = kiwi.retrieve(kiwi_query)
            prompt = f"\n\nDoplněné informace o letech:\n{kiwi_result}\n\nOdpověz na původní dotaz: {prompt}"
        else:
            break

    print(response)