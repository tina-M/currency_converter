# currency_converter

Scrapes http://www.nbs.sk/sk/statisticke-udaje/kurzovy-listok/denny-kurzovy-listok-ecb (The Central Bank of the Slovak Republic) via *BeautifulSoup* and loads actual exchange rate into the dictionary in form **'currency': 'value'**. 

All currencies are quoted against the euro (base currency).

### Command-line parameters:

    -- amount 
    
    -- input_currency - 3 letters or symbol
    
    -- output_currency - 3 letters or symbol 

- If *output_currency* parameter is missing, converts to all known currencies.

- If *input/output_currency* parameter is unknown, exits the program.

- If *amount* parameter is not number, exits.

- If currency symbol belongs to more than one currency, converts to all corresponding currencies.



### Output for **'currency_converter.py --amount 100 --input_currency $  --output_currency CZK'**:

(the symbol **$** belongs to 6 currencies, so it converts all these currencies to **CZK**)

```
{
   "input": {
      "currency": "CAD",      
      "amount": 100.0
   }, 
   "output": {
      "CZK": 1776.58
   },   
   
   "input1": {
      "currency": "USD",      
      "amount": 100.0
   }, 
   "output1": {
      "CZK": 2349.15
   }, 
   
   "input2": {
      "currency": "MXN", 
      "amount": 100.0
   }, 
   "output2": {
      "CZK": 130.59
   },
   
   "input3": {
      "currency": "AUD", 
      "amount": 100.0
   }, 
   "output3": {
      "CZK": 1786.62
   },
   
   "input4": {
      "currency": "SGD", 
      "amount": 100.0
   }, 
   "output4": {
      "CZK": 1697.16
   },
   
   "input5": {
      "currency": "NZD", 
      "amount": 100.0
   },  
   "output5": {
      "CZK": 1698.92
   },
}
```
