import sys
import getopt
import urllib.request
from bs4 import BeautifulSoup


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
    currency_table = scrape_web_page()
    exchange_rate = {}
    for row in currency_table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) == 5:
            value = cells[2].find(text=True).strip("\r\n\t ").replace("\xa0", "").replace(",", ".")
            currency = cells[0].find(text=True).strip(" ")
            try:
                float_value = float(value)
                exchange_rate[currency] = float_value
            except ValueError:
                # print(currency + " - no value")
                continue

    return exchange_rate


amount = 0.0
input_currency = ""
output_currency = ""

options, args = getopt.getopt(sys.argv[1:], "", ["amount=", "input_currency=", "output_currency="])

for opt, args in options:
    if opt == "--amount":
        amount = args
        continue
    if opt == "--input_currency":
        input_currency = args
        continue
    if opt == "--output_currency":
        output_currency = args
        continue

print(amount)
print(input_currency)
print(output_currency)

exchange_rate = create_exchange_rate()
#print(exchange_rate)
