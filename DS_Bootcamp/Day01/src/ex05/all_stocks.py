import sys

def parser(str):
    answer = ['']
    index = 0
    last_was_comma = 0
    for ch in str:
        if (ch == ',') and (last_was_comma == 1):
            return 0
        elif (ch == ',') and (last_was_comma == 0):
            index += 1
            answer.append('')
            last_was_comma = 1
        elif not(ch == ' '):
            answer[index] += ch
            last_was_comma = 0
    if last_was_comma == 1:
        return 0
    else:
        return answer

def print_for_ticker(first, second):
    print(f"{first} is a ticker symbol for {second}")

def print_for_stock(first, second):
    print(f"{first} stock price as {second}")

def print_for_unknown(word):
    print(f"{word} as an unknown company or an unknown ticker sumbol")

def format_for_company(str):
    answer = str[0].upper()
    if (len(str)>1):
        answer += str[1:].lower()
    return answer

def format_for_ticker(str):
    return str.upper()

def check_dictionares(words):
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

    for word in words:
        if (format_for_company(word) in COMPANIES.keys()):
            print_for_stock(format_for_company(word), STOCKS[COMPANIES[format_for_company(word)]])
        elif (format_for_ticker(word) in reverse_COMPANY.keys()):
            print_for_ticker(format_for_ticker(word), reverse_COMPANY[format_for_ticker(word)])
        else:
            print_for_unknown(word)


def all_stocks():
    arguments = sys.argv
    if (len(arguments) == 2):
        words = parser(arguments[1])
        if not(words == 0):
            check_dictionares(words)


if __name__ == '__main__':
    all_stocks()