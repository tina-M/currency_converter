import urllib.request
from bs4 import BeautifulSoup

with urllib.request.urlopen("http://www.nbs.sk/sk/statisticke-udaje/kurzovy-listok/denny-kurzovy-listok-ecb") as url:
    page = url.read()

soup = BeautifulSoup(page, "lxml")
#print(soup.prettify())
trs = soup.find_all("tr")
currency_table = soup.find('table', class_='tblBorder')

currency = []
currency_code = []
value = []

for row in currency_table.findAll("tr"):
    cells = row.findAll("td")
    if len(cells) == 5:
        currency_code.append(cells[0].find(text=True))
        currency.append(cells[1].find(text=True))
        value.append(cells[2].find(text=True))

print(currency_code)
print(currency)
print(value)
