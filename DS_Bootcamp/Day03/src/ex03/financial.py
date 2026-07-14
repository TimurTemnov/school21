#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import sys
import time

def main():
    if len(sys.argv) != 3:
        raise Exception("Wrong Number of ARGs")
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}
    url = f'https://finance.yahoo.com/quote/{sys.argv[1]}/financials/'
    response = requests.get(url, headers=headers)
    bs = BeautifulSoup(response.text, 'html.parser')
    title_of_page = bs.title.string
    if title_of_page == 'Symbol Lookup from Yahoo Finance':
        raise Exception('Wrong ticker')
    
    table_body = bs.find(class_ = 'tableBody')
    rows_of_table = table_body.find_all(class_ = 'row')
    check_title = []
    for row in rows_of_table:
        check_title.append(row.find(class_ = 'rowTitle').text)
    if sys.argv[2] not in check_title:
        raise Exception("Wrong field of table")
    time.sleep(5)

    answer_row = 0
    for row in rows_of_table:
        if sys.argv[2] == row.find(class_ = 'rowTitle').text:
            answer_row = row

    answer = [sys.argv[2]]

    columns = answer_row.find_all(class_ = 'column')
    for col in columns[1:]:
        answer.append(col.text)

    print(tuple(answer))

    

if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print(type(err).__name__, err, sep=':=')
