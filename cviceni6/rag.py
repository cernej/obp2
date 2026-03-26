import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod


class RAG(ABC):
    @abstractmethod
    def retrieve(self, query: str) -> str:
        pass


class WikiRAG(RAG):
    SEARCH_URL = "https://search.seznam.cz/"
    HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

    def retrieve(self, query: str) -> str:
        search_query = f"{query} site:cs.wikipedia.org"
        response = requests.get(
            self.SEARCH_URL,
            params={"q": search_query},
            headers=self.HEADERS,
            timeout=10,
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        wiki_url = None
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "cs.wikipedia.org/wiki/" in href:
                wiki_url = href
                break

        if not wiki_url:
            return ""

        wiki_response = requests.get(wiki_url, headers=self.HEADERS, timeout=10)
        wiki_response.raise_for_status()

        wiki_soup = BeautifulSoup(wiki_response.text, "html.parser")

        content_div = wiki_soup.find("div", {"id": "mw-content-text", "class": "mw-body-content"})
        if not content_div:
            return ""

        paragraphs = content_div.find_all("p", id=lambda x: x and x.startswith("mw"))
        return "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))


class WeatherRAG(RAG):
    API_URL = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
    HEADERS = {"User-Agent": "pef-weather-rag/1.0 github.com/cernej/pef"}

    SYMBOL_CODES = {
        "clearsky": "jasno",
        "fair": "převážně jasno",
        "partlycloudy": "částečná oblačnost",
        "cloudy": "zataženo",
        "fog": "mlha",
        "rainshowers": "přeháňky",
        "heavyrainshowers": "silné přeháňky",
        "lightrainshowers": "slabé přeháňky",
        "rain": "déšť",
        "heavyrain": "silný déšť",
        "lightrain": "slabý déšť",
        "sleet": "déšť se sněhem",
        "snow": "sníh",
        "heavysnow": "silný sníh",
        "lightsnow": "slabý sníh",
        "snowshowers": "sněhové přeháňky",
        "thunderstorm": "bouřka",
        "thunder": "hrom",
    }

    def retrieve(self, query: str) -> str:
        parts = query.strip().split(",")
        if len(parts) != 2:
            return "Chybný formát dotazu. Použij 'zemepisna_sirka,zemepisna_delka'."
        try:
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
        except ValueError:
            return "Chybné souřadnice, očekávána čísla."

        response = requests.get(
            self.API_URL,
            params={"lat": round(lat, 4), "lon": round(lon, 4)},
            headers=self.HEADERS,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        timeseries = data["properties"]["timeseries"]
        current = timeseries[0]
        instant = current["data"]["instant"]["details"]
        next_1h = current["data"].get("next_1_hours", {})
        symbol_code = next_1h.get("summary", {}).get("symbol_code", "")
        precip = next_1h.get("details", {}).get("precipitation_amount", 0.0)

        temp = instant.get("air_temperature")
        feels_like = instant.get("wind_speed")
        humidity = instant.get("relative_humidity")
        wind_speed = instant.get("wind_speed")
        wind_dir = instant.get("wind_from_direction")
        pressure = instant.get("air_pressure_at_sea_level")

        # resolve symbol to Czech description
        base_code = symbol_code.split("_")[0] if symbol_code else ""
        description = self.SYMBOL_CODES.get(base_code, symbol_code or "neznámo")

        lines = [f"Počasí pro souřadnice {lat}, {lon}:"]
        lines.append(f"Stav: {description}")
        if temp is not None:
            lines.append(f"Teplota: {temp} °C")
        if humidity is not None:
            lines.append(f"Vlhkost: {humidity} %")
        if wind_speed is not None:
            direction = f", směr {wind_dir}°" if wind_dir is not None else ""
            lines.append(f"Vítr: {wind_speed} m/s{direction}")
        if pressure is not None:
            lines.append(f"Tlak: {pressure} hPa")
        if precip:
            lines.append(f"Srážky (příští 1 h): {precip} mm")

        return "\n".join(lines)


class RateRAG(RAG):
    CNB_URL = "https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt"
    HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}

    def retrieve(self, query: str) -> str:
        codes = [c.strip().upper() for c in query.split(",") if c.strip()]
        if not codes:
            return "Zadej alespoň jeden kód měny, např. 'EUR,USD'."

        response = requests.get(self.CNB_URL, headers=self.HEADERS, timeout=10)
        response.raise_for_status()
        text = response.text

        lines = text.splitlines()
        # first line: date, second: header, rest: data
        date_line = lines[0] if lines else ""
        rates = {}
        for line in lines[2:]:
            parts = line.split("|")
            if len(parts) != 5:
                continue
            country, currency, amount, code, rate = parts
            try:
                rates[code.strip()] = {
                    "country": country.strip(),
                    "currency": currency.strip(),
                    "amount": int(amount.strip()),
                    "rate": float(rate.strip().replace(",", ".")),
                }
            except ValueError:
                continue

        result_lines = [f"Kurzy ČNB ({date_line.split()[0]}):"]
        for code in codes:
            if code == "CZK":
                result_lines.append("CZK: 1,000 Kč (domácí měna)")
            elif code in rates:
                r = rates[code]
                result_lines.append(
                    f"{code} ({r['currency']}, {r['country']}): "
                    f"{r['amount']} {code} = {r['rate']:.3f} CZK"
                )
            else:
                result_lines.append(f"{code}: nenalezeno v kurzovním lístku ČNB")

        return "\n".join(result_lines)


if __name__ == "__main__":
    rag = WikiRAG()
    query = "volby do poslanecke snemovny 2025"
    result = rag.retrieve(query)
    print(result)