import sys
import getopt
import urllib.request
from bs4 import BeautifulSoup

CURRENCY_SYMBOLS = {'HUF': 'Ft', 'MYR': 'RM', 'JPY': '¥', 'USD': '$', 'SEK': 'kr', 'KRW': '₩', 'NZD': '$', 'CHF': 'CHF',
                    'SGD': '$', 'RON': 'lei', 'CNY': '¥', 'CZK': 'Kč', 'BRL': 'R$', 'RUB': '₽', 'BGN': 'лв', 'ILS': '₪',
                    'MXN': '$', 'THB': '฿', 'HRK': 'kn', 'GBP': '£', 'DKK': 'kr', 'TRY': '₺', 'CAD': '$', 'NOK': 'kr',
                    'ZAR': 'R', 'HKD': 'HK$', 'AUD': '$', 'INR': '₹', 'PLN': 'zł', 'IDR': 'Rp', 'PHP': '₱'}


# access to web page of the Central bank of the Slovak Republic and load content - the table of exchange rate
def scrape_web_page():
    with urllib.request.urlopen(
            "http://www.nbs.sk/sk/statisticke-udaje/kurzovy-listok/denny-kurzovy-listok-ecb") as url:
        page = url.read()

    soup = BeautifulSoup(page, "lxml")
    currency_table = soup.find('table', class_='tblBorder')

    return currency_table


# from the table of exchange rate create the dictionary - <currency> : <amount>
def create_exchange_rate():
    cur = []
    currency_table = scrape_web_page()
    exchange_rate = {}
    for row in currency_table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) == 5:
            value = cells[2].find(text=True).strip("\r\n\t ").replace("\xa0", "").replace(",", ".")
            currency = cells[0].find(text=True).strip(" ")
            try:
                float_value = float(value)
                cur.append(currency)
                exchange_rate[currency] = float_value
            except ValueError:
                # print(currency + " - no value")
                continue

    return exchange_rate


# EUR -> xxx
def from_eur(amount, to_currency):
    rate = exchange_rate.get(to_currency)
    return amount * rate


# xxx -> EUR
def to_eur(amount, from_currency):
    rate = exchange_rate.get(from_currency)
    return amount / rate


def parse_commandline_parameters():
    amount = 0.0
    input_cur = ""
    output_cur = ""
    
    options, args = getopt.getopt(sys.argv[1:], "", ["amount=", "input_currency=", "output_currency="])
    
    for opt, args in options:
        if opt == "--amount":
            amount = args
            continue
        if opt == "--input_currency":
            input_cur = args
            continue
        if opt == "--output_currency":
            output_cur = args
        continue
    
    return amount, input_cur, output_cur


def is_currency_symbol(currency):
    satisfactory_currencies = []
    if currency not in list(CURRENCY_SYMBOLS.keys()):  # maybe input_currency == any symbol?
        for cur, symbol in CURRENCY_SYMBOLS.items():
            if symbol == currency:
                satisfactory_currencies.append(cur)

        if len(satisfactory_currencies) == 0:   # original currency
            print("Unknown currency!")
            exit(1)
        else:
            return satisfactory_currencies
    return [currency]



amount, input_cur, output_cur = parse_commandline_parameters()
exchange_rate = create_exchange_rate()
#print(exchange_rate)

print(amount)
print(input_cur)
print(output_cur)

input_currency = is_currency_symbol(input_cur)
if len(output_cur) != 0:
    output_currency = is_currency_symbol(output_cur)
else:  # output_currency parameter missing - convert to all known currencies
    output_currency = list(exchange_rate.keys())

print(input_currency)
print(output_currency)
