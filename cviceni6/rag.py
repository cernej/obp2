import os
import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from datetime import datetime


class RAG(ABC):
    @abstractmethod
    def retrieve(self, query: str) -> str:
        pass


class WikiRAG(RAG):
    SEARCH_URL = "https://search.seznam.cz/"
    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.3"}

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


class KiwiRAG(RAG):
    API_URL = "https://tequila-api.kiwi.com/v2/search"

    def __init__(self, api_key: str):
        self.api_key = api_key.strip()

    def _parse_date(self, value: str) -> str | None:
        date_str = value.strip()
        for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(date_str, fmt).strftime("%d/%m/%Y")
            except ValueError:
                continue
        return None

    def retrieve(self, query: str) -> str:
        if not self.api_key:
            return "Chybi KIWI_API_KEY. Nastav environment promennou pro pristup do Kiwi API."

        parts = [p.strip() for p in query.split(",")]
        if len(parts) != 3:
            return "Chybny format dotazu. Pouzij 'odkud,kam,kdy' (napr. PRG,BCN,2026-05-20)."

        fly_from = parts[0].upper()
        fly_to = parts[1].upper()
        if len(fly_from) != 3 or len(fly_to) != 3:
            return "Prozatim podporuji IATA kody letist (3 pismena), napr. PRG,BCN,2026-05-20."

        flight_date = self._parse_date(parts[2])
        if not flight_date:
            return "Chybny format data. Pouzij YYYY-MM-DD, DD.MM.YYYY nebo DD/MM/YYYY."

        # Kiwi API byva citlive na kombinace parametru; zkusime 2 bezne varianty datumu.
        date_variants = [flight_date]
        try:
            date_variants.append(datetime.strptime(flight_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
        except ValueError:
            pass

        payload = None
        last_error = ""
        for date_value in date_variants:
            response = requests.get(
                self.API_URL,
                params={
                    "fly_from": fly_from,
                    "fly_to": fly_to,
                    "date_from": date_value,
                    "date_to": date_value,
                    "limit": 5,
                    "curr": "CZK",
                    "sort": "price",
                    "adults": 1,
                    "flight_type": "oneway",
                },
                headers={"apikey": self.api_key},
                timeout=10,
            )

            if response.ok:
                payload = response.json()
                break

            try:
                error_json = response.json()
                last_error = error_json.get("message") or str(error_json)
            except ValueError:
                last_error = response.text.strip()[:300]

        if payload is None:
            return (
                "Kiwi API vratilo chybu pri hledani letu. "
                f"Zkontroluj KIWI_API_KEY a format dotazu 'ODKUD,KAM,KDY'. Detaily: {last_error or 'neuvedeno'}"
            )

        flights = payload.get("data", [])
        if not flights:
            return f"Nenalezeny zadne lety pro trasu {fly_from}->{fly_to} na {flight_date}."

        lines = [f"Nalezeno {len(flights)} letu pro {fly_from}->{fly_to} ({flight_date}):"]
        for idx, item in enumerate(flights, start=1):
            city_from = item.get("cityFrom", "?")
            code_from = item.get("flyFrom", fly_from)
            city_to = item.get("cityTo", "?")
            code_to = item.get("flyTo", fly_to)
            departure = (item.get("local_departure") or "").replace("T", " ")[:16]
            arrival = (item.get("local_arrival") or "").replace("T", " ")[:16]
            price = item.get("price", "?")
            currency = item.get("currency", "CZK")
            airlines = ",".join(item.get("airlines", [])) or "?"
            deep_link = item.get("deep_link", "")

            lines.append(
                f"{idx}. {city_from} ({code_from}) -> {city_to} ({code_to}), "
                f"odlet {departure}, prilet {arrival}, cena {price} {currency}, dopravce {airlines}"
            )
            if deep_link:
                lines.append(f"   Rezervace: {deep_link}")

        return "\n".join(lines)


if __name__ == "__main__":
    # rag = WikiRAG()
    # query = "volby do poslanecke snemovny 2025"
    # result = rag.retrieve(query)
    # print(result)
    # rag = WeatherRAG()
    # query = "50.0755,14.4378"  # Praha
    # result = rag.retrieve(query)
    # print(result)
    rag = KiwiRAG(os.getenv("KIWI_API_KEY", ""))
    query = "PRG,BCN,20/05/2026"
    result = rag.retrieve(query)
    print(result)