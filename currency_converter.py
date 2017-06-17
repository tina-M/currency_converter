import urllib.request
from bs4 import BeautifulSoup


def create_exchange_rate():
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


with urllib.request.urlopen("http://www.nbs.sk/sk/statisticke-udaje/kurzovy-listok/denny-kurzovy-listok-ecb") as url:
    page = url.read()

soup = BeautifulSoup(page, "lxml")
# print(soup.prettify())
trs = soup.find_all("tr")
currency_table = soup.find('table', class_='tblBorder')

exchange_rate = create_exchange_rate()
print(exchange_rate)
