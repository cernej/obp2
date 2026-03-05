import requests
from datetime import datetime

CNB_URL = 'https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt'

def fetch_exchange_rates():
    response = requests.get(CNB_URL)
    if response.status_code == 200:
        data = response.text.splitlines()
        date_str = data[0].split(' ')[0]
        date = datetime.strptime(date_str, '%d.%m.%Y').date()
        rates = {}
        for line in data[2:]:
            parts = line.split('|')
            if len(parts) >= 5:
                currency_code = parts[3]
                amount = int(parts[2])
                exchange_rate = float(parts[4].replace(',', '.')) / amount
                rates[currency_code] = (amount, exchange_rate)
        return date, rates
    else:
        raise Exception(f'Failed to fetch exchange rates: {response.status_code}')


if __name__ == '__main__':
    date, rates = fetch_exchange_rates()
    print(f'Exchange rates for {date}:')
    for code, (amount, rate) in rates.items():
        print(f'{code}: {amount} {code} = {rate:.4f} CZK')