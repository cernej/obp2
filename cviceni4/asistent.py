import google.generativeai as genai
import os
from abc import ABC, abstractmethod


class Asistent(ABC):
    def __init__(self, api_key, model_name='gemini-2.5-flash'):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.system_prompt = ''
    
    def set_system_prompt(self, prompt):
        self.system_prompt = prompt
    
    def generate_content(self, prompt):
        response = self.model.generate_content(self.system_prompt + prompt)
        return response.text


class VIPAsistent(Asistent):
    def __init__(self, api_key, model_name='gemini-2.5-flash'):
        super().__init__(api_key, model_name)
        self.set_system_prompt("""
Chovej se jako Milos Zeman a pri kazde otazce vyjadri, ze je tazatel hloupejsi nez ty.
Otazka na tebe:
""")


class Vyzkumnik(Asistent):
    def __init__(self, api_key, model_name='gemini-2.5-flash'):
        super().__init__(api_key, model_name)
        self.set_system_prompt("""
Jsi vyzkumny pracovnik. Sanzis se prijit s novym neotrelym resenim.
Vse, co navrhujes podkladas nejakymi vedeckymi poznatky a doplnujes o zdroje.
Ukol pro tebe:
""")


class Kritik(Asistent):
    def __init__(self, api_key, model_name='gemini-2.5-flash'):
        super().__init__(api_key, model_name)
        self.set_system_prompt("""
Jsi kritik. V predlozenem vyzkum se snazis najit nedostatky a navrhnout, jak by se daly vylepsit.
Tady je vyzkum:
""")
        

class Korektor(Asistent):
    def __init__(self, api_key, model_name='gemini-2.5-flash'):
        super().__init__(api_key, model_name)
        self.set_system_prompt("""
Jsi korektor, dostanes text od vyzkumnika a poznamky kritika a na zaklade nich udelas finalni vystup.
Text vyzkumnika a kritika:
""")