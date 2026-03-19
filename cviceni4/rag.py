from abc import ABC, abstractmethod
import requests


class RAG(ABC):
    def __init__(self, url):
        self.url = url
    
    @abstractmethod
    def search(self, query: str) -> str:
        pass


class RAGNovinky(RAG):
    def search(self, query: str) -> str:
        response = requests.get(self.url)
        if not response.ok:
            return ''
        content = response.text
        # TODO: vyparsovani podstatnych informaci
        return content


class RAGPocasi(RAG):
    def search(self, query: str) -> str:
        # predpoklad v query je "latitude,longitude"
        latitude, longitude = [float(x.strip()) for x in query.split(',')]
        url = self.url.format(latitude, longitude)
        response = requests.get(url, headers={"User-Agent": "moje-aplikace/1.0 (email@example.com)"})
        if not response.ok:
            return ''
        return response.text
        

if __name__ == '__main__':
    # r = RAGNovinky('https://api-web.novinky.cz/v1/timelines/62baab43a1bac57b7436dc07?xml=rss')
    # print(r.search(''))
    r = RAGPocasi('https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={}&lon={}')
    print(r.search('48.9747,14.4745'))