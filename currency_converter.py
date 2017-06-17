import sys
import getopt
import urllib.request
import json
from bs4 import BeautifulSoup

CURRENCY_SYMBOLS = {'HUF': 'Ft', 'MYR': 'RM', 'JPY': '¥', 'USD': '$', 'SEK': 'kr', 'KRW': '₩', 'NZD': '$', 'CHF': 'CHF',
                    'SGD': '$', 'RON': 'lei', 'CNY': '¥', 'CZK': 'Kč', 'BRL': 'R$', 'RUB': '₽', 'BGN': 'лв', 'ILS': '₪',
                    'MXN': '$', 'THB': '฿', 'HRK': 'kn', 'GBP': '£', 'DKK': 'kr', 'TRY': '₺', 'CAD': '$', 'NOK': 'kr',
                    'ZAR': 'R', 'HKD': 'HK$', 'AUD': '$', 'INR': '₹', 'PLN': 'zł', 'IDR': 'Rp', 'PHP': '₱', 'EUR': '€'}


# access to web page of the Central bank of the Slovak Republic and load content - the table of exchange rate
def scrape_web_page():
    with urllib.request.urlopen(
            'http://www.nbs.sk/sk/statisticke-udaje/kurzovy-listok/denny-kurzovy-listok-ecb') as url:
        page = url.read()

    soup = BeautifulSoup(page, 'lxml')
    currency_table = soup.find('table', class_='tblBorder')

    return currency_table


# from the table of exchange rate create the dictionary - <currency> : <amount>
def create_exchange_rate():
    cur = []
    currency_table = scrape_web_page()
    exchange_rate = {}
    for row in currency_table.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) == 5:
            value = cells[2].find(text=True).strip('\r\n\t ').replace('\xa0', '').replace(',', '.')
            currency = cells[0].find(text=True).strip(' ')
            try:
                float_value = float(value)
                cur.append(currency)
                exchange_rate[currency] = float_value
            except ValueError:
                continue  # currency with no value in the table

    return exchange_rate


# EUR -> xxx
def from_eur(amount, to_currency):
    rate = exchange_rate.get(to_currency)
    return amount * float(rate)


# xxx -> EUR
def to_eur(amount, from_currency):
    rate = exchange_rate.get(from_currency)
    return amount / float(rate)


def parse_commandline_parameters():
    amount = 0.0
    input_cur = ''
    output_cur = ''
    
    options, args = getopt.getopt(sys.argv[1:], '', ['amount=', 'input_currency=', 'output_currency='])
    
    for opt, args in options:
        if opt == '--amount':
            try:
                amount = float(args)
                continue
            except ValueError:
                print("Not number in amount parameter!")
                exit(2)
        if opt == '--input_currency':
            input_cur = args
            continue
        if opt == '--output_currency':
            output_cur = args
            continue
    
    return amount, input_cur, output_cur


# check whether currency is symbol
# if True, convert to all currencies with the same symbol
# if False, return original currency
# if currency is not symbol & currency is not in the list of known currencies, exit(1)
def is_currency_symbol(currency):
    satisfactory_currencies = []
    if currency not in list(CURRENCY_SYMBOLS.keys()):  # maybe input_currency == any symbol?
        for cur, symbol in CURRENCY_SYMBOLS.items():
            if symbol == currency:
                satisfactory_currencies.append(cur)

        if len(satisfactory_currencies) == 0:
            print('Unknown currency!')
            exit(1)
        else:
            return satisfactory_currencies
    return [currency]


# convert input_currency to output_currency
# xxx -> EUR -> yyy because the euro is base currency
def convert(amount, input_currency, output_currency):
    if input_currency == 'EUR':
        res = from_eur(amount, output_currency)
    elif output_currency == 'EUR':
        res = to_eur(amount, input_currency)
    else:
        tmp_res = to_eur(amount, input_currency)
        res = from_eur(tmp_res, output_currency)

    return res


# convert all input_currencies to all output_currencies (round to 2 decimal places)
# if currency symbol belong to more than one currency (e.g. '$'), convert to all corresponding currencies
# if there is not any output_currency parameter, convert to all known currencies
# conversion options:  1 -> 1 / 1 -> M (one to many) / M -> 1 / M -> N (many to many)
# in case of M -> x option, resultant json is in the form: 'inputX = {}, outputX = {}' where X is the serial
# number of result (first result has not number, second result = 1...)
# e.g. {"input": {"amount": 100.0, "currency": "MXN"}, "output": {"CZK": 130.59},
#       "input1": {"amount": 100.0, "currency": "NZD"}, "output1": {"CZK": 1698.92}}
def convert_all():
    output_json = {}
    i = 0
    for i_currency in input_currency:
        o_dict = {}
        for o_currency in output_currency:
            if i_currency == o_currency:
                o_dict[o_currency] = float(format(amount, '.2f'))
            else:
                o_dict[o_currency] = float(format(convert(amount, i_currency, o_currency), '.2f'))

        if i == 0:
            output_json['input'] = {'amount': amount, 'currency': i_currency}
            output_json['output'] = o_dict
        else:
            output_json['input' + str(i)] = {'amount': amount, 'currency': i_currency}
            output_json['output' + str(i)] = o_dict
        i += 1

    return output_json


if __name__ == "__main__":
    amount, input_cur, output_cur = parse_commandline_parameters()
    exchange_rate = create_exchange_rate()

    input_currency = is_currency_symbol(input_cur)
    if len(output_cur) != 0:
        output_currency = is_currency_symbol(output_cur)
    else:  # output_currency parameter missing - convert to all known currencies
        output_currency = list(exchange_rate.keys())

    print(json.dumps(convert_all()))