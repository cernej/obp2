import sys
from asistent import Vyzkumnik, Kritik, Korektor, ZemanAI, NewsAsistent
from rag import RAGNovinky, RAGPocasi

# API_KEY ziskate na https://aistudio.google.com/

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} vas_dotaz')
        sys.exit(1)

    dotaz = sys.argv[1]

    news = NewsAsistent("AIzaSyDCr9Y5lRjxD2xGoiZ-r60Z8w9acDRQJM8")
    rag_novinky = RAGNovinky('https://api-web.novinky.cz/v1/timelines/62baab43a1bac57b7436dc07?xml=rss')
    rag_pocasi = RAGPocasi('https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={}&lon={}')

    rags = {'NEWS': rag_novinky, 'WEATHER': rag_pocasi}

    tmp_dotaz = dotaz

    count = 0
    while True:
        print(f'Nas aktualni dotaz: {tmp_dotaz}')
        odpoved = news.generate_content(tmp_dotaz)
        if 'NEWS:' not in odpoved and 'WEATHER:' not in odpoved:
            break
        print(f'Asistent se nas pta na: "{odpoved}"')
        if 'NEWS:' in odpoved:
            odpoved = odpoved.split('NEWS:')[1]
            if '"' in odpoved:
                odpoved = odpoved.split('"')[1]
            vysledek = rag_novinky.search(odpoved)
            tmp_dotaz = dotaz + "\nRESULTS:\n" + vysledek
        elif 'WEATHER:' in odpoved:
            odpoved = odpoved.split('WEATHER:')[1]
            if '"' in odpoved:
                odpoved = odpoved.split('"')[1]
            vysledek = rag_pocasi.search(odpoved)
            tmp_dotaz = dotaz + "\nRESULTS:\n" + vysledek
        count += 1
        if count > 3:
            break
    
    print(f'Odpoved asistenta: {odpoved}')

    # zeman = ZemanAI("AIzaSyDCr9Y5lRjxD2xGoiZ-r60Z8w9acDRQJM8")
    # odpoved = zeman.generate_content("Jak se mate v duchodu?")
    # print(odpoved)


    # vyzkumnik = Vyzkumnik("API_KEY")
    # kritik = Kritik("API_KEY")
    # korektor = Korektor("API_KEY")
    
    # zadani = "Jak nejsnadneji dostudovat EF JCU?"

    # odpoved = vyzkumnik.generate_content(zadani)

    # print(odpoved)

    # kritika = kritik.generate_content(odpoved)

    # print(kritika)

    # vysledek = korektor.generate_content(odpoved + "\n" + kritika)

    # print(vysledek)
