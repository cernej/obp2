from urllib.parse import urljoin
import json
import re
import requests
from bs4 import BeautifulSoup

URL = "https://www.pelikan.cz/cs/akcni-letenky/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

PRICE_RE = re.compile(r"(\d[\d\s\xa0.,]*)\s*(Kc|Kč|EUR|€|USD|\$)", re.IGNORECASE)
ROUTE_IATA_RE = re.compile(r"\b([A-Z]{3})\s*(?:-|–|->|>|→)\s*([A-Z]{3})\b")
ROUTE_CITY_RE = re.compile(
    r"\b([A-ZÁ-Ž][A-Za-zÁ-ž\s.-]{2,})\s*(?:-|–|->|>|→)\s*([A-ZÁ-Ž][A-Za-zÁ-ž\s.-]{2,})\b"
)
AIRLINE_KEYWORDS = [
    "Ryanair",
    "Wizz Air",
    "easyJet",
    "Smartwings",
    "Lufthansa",
    "KLM",
    "Eurowings",
    "LOT",
    "Aegean",
    "Qatar Airways",
    "Turkish Airlines",
    "Emirates",
    "British Airways",
    "Air France",
    "Vueling",
]


def normalize_text(value: str) -> str:
    return " ".join(value.replace("\xa0", " ").split())


def fetch_html(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.text


def extract_price(text: str) -> str:
    match = PRICE_RE.search(text)
    if not match:
        return ""
    amount = normalize_text(match.group(1)).replace(" ", "")
    currency = match.group(2)
    return f"{amount} {currency}"


def extract_route(text: str) -> tuple[str, str]:
    iata_match = ROUTE_IATA_RE.search(text)
    if iata_match:
        return iata_match.group(1), iata_match.group(2)

    city_match = ROUTE_CITY_RE.search(text)
    if city_match:
        return city_match.group(1).strip(), city_match.group(2).strip()

    return "", ""


def extract_airline(text: str) -> str:
    for airline in AIRLINE_KEYWORDS:
        if re.search(rf"\b{re.escape(airline)}\b", text, flags=re.IGNORECASE):
            return airline
    return ""


def build_offer(text: str, href: str) -> dict | None:
    normalized = normalize_text(text)
    price = extract_price(normalized)
    if not price:
        return None

    origin, destination = extract_route(normalized)
    airline = extract_airline(normalized)

    return {
        "odkud": origin,
        "kam": destination,
        "cena": price,
        "letecka_spolecnost": airline,
        "odkaz": href,
    }


def extract_from_json_ld(soup: BeautifulSoup, base_url: str) -> list[dict]:
    offers = []

    def walk(node):
        if isinstance(node, dict):
            href = node.get("url") or node.get("link") or node.get("href") or node.get("@id") or ""
            if href:
                href = urljoin(base_url, href)

            # Heuristika: mnoho webů drží detaily letu přímo v JSON-LD,
            # proto dict převádíme na text a vytáhneme trasu/cenu/dopravce regexem.
            raw = json.dumps(node, ensure_ascii=False)
            offer = build_offer(raw, href)
            if offer:
                offers.append(offer)

            for value in node.values():
                walk(value)

        elif isinstance(node, list):
            for item in node:
                walk(item)

    for script in soup.find_all("script", type="application/ld+json"):
        script_text = script.string or script.get_text(strip=True)
        if not script_text:
            continue

        try:
            data = json.loads(script_text)
        except json.JSONDecodeError:
            continue

        walk(data)

    return offers


def extract_from_dom(soup: BeautifulSoup, base_url: str) -> list[dict]:
    offers = []
    selectors = [
        "article",
        "li",
        "div.card",
        "div[class*='deal']",
        "div[class*='flight']",
        "div[class*='offer']",
    ]

    for selector in selectors:
        for element in soup.select(selector):
            text = element.get_text(" ", strip=True)
            if len(text) < 25:
                continue

            anchor = element.find("a", href=True)
            href = urljoin(base_url, anchor["href"]) if anchor else base_url
            offer = build_offer(text, href)
            if offer:
                offers.append(offer)

    return offers


def deduplicate(offers: list[dict]) -> list[dict]:
    unique = []
    seen = set()

    for offer in offers:
        key = (
            offer.get("odkud", ""),
            offer.get("kam", ""),
            offer.get("cena", ""),
            offer.get("letecka_spolecnost", ""),
            offer.get("odkaz", ""),
        )
        if key in seen:
            continue

        # Filtr proti šumu: aspoň trasa nebo letecká společnost musí být známá.
        if not (offer["odkud"] and offer["kam"]) and not offer["letecka_spolecnost"]:
            continue

        seen.add(key)
        unique.append(offer)

    return unique


def parse_akcni_letenky(url: str = URL) -> list[dict]:
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    offers = []
    offers.extend(extract_from_json_ld(soup, url))
    offers.extend(extract_from_dom(soup, url))
    return deduplicate(offers)


if __name__ == "__main__":
    try:
        deals = parse_akcni_letenky(URL)
        if not deals:
            print("Žádné akční letenky se nepodařilo vytěžit. Zkontroluj selektory nebo strukturu stránky.")
        else:
            print(f"Nalezeno {len(deals)} akčních letenek:\n")
            for i, deal in enumerate(deals, start=1):
                print(
                    f"{i}. {deal['odkud']} -> {deal['kam']} | "
                    f"{deal['cena']} | {deal['letecka_spolecnost']} | {deal['odkaz']}"
                )

            with open("akcniletenky.json", "w", encoding="utf-8") as f:
                json.dump(deals, f, ensure_ascii=False, indent=2)
            print("\nVýstup uložen do akcniletenky.json")

    except Exception as exc:
        print(f"Chyba parseru: {exc}")