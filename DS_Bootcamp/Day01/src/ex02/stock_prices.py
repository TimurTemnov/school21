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

    price = 0

    check_str = str[0].upper()
    if (len(str) > 1):
        check_str += str[1:].lower()
    if (check_str in COMPANIES.keys()):
        price = STOCKS[COMPANIES[check_str]]
    return price

def stock_prices():
    arguments = sys.argv
    if (len(arguments) == 2):
        answer = answer_from_dict(arguments[1])
        if (answer == 0):
            print('Unknown company')
        else:
            print(answer)


if __name__ == '__main__':
    stock_prices()