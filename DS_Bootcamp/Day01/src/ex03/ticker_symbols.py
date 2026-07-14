import sys

def answer_from_dict(str):
    COMPANIES = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Netflix': 'NFLX',
    'Tesla': 'TSLA',
    'Nokia': 'NOK'
    }

    STOCKS = {
    'AAPL': 287.73,
    'MSFT': 173.79,
    'NFLX': 416.90,
    'TSLA': 724.88,
    'NOK': 3.37
    }

    reverse_COMPANY = dict(zip(COMPANIES.values(), COMPANIES.keys()))
  
    check_str = str.upper()
    price = 0
    company = ""

    if (check_str in STOCKS.keys()):
        price = STOCKS[check_str]
        company = reverse_COMPANY[check_str]
    return  company, price

def ticker_symbols():
    arguments = sys.argv
    if (len(arguments) == 2):
        company, price = answer_from_dict(arguments[1])
        if (price == 0):
            print('Unknown company')
        else:
            print(company, price)

if __name__ == '__main__':
    ticker_symbols()