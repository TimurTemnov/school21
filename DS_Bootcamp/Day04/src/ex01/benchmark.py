#!/usr/bin/env python3

import timeit

def loop(gmails: list):
    answer_list = []
    for email in gmails:
        if email.endswith('gmail.com'):
            answer_list.append(email)
    return answer_list

def list_comprehension(gmails: list):
    return [email for email in gmails if email.endswith('gmail.com')]

def map_for_list(gmails: list):
    result = map(lambda x: x if x.endswith('gmail.com') else None, gmails)
    return result

def main():
    setup = """
from __main__ import loop, list_comprehension, map_for_list
emails = 5 * ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com']
"""
    stmt = ['loop(emails)', 'list_comprehension(emails)', 'map_for_list(emails)']
    number = 90000#00

    time_1 = timeit.timeit(setup=setup, stmt=stmt[0], number=number)
    time_2 = timeit.timeit(setup=setup, stmt=stmt[1], number=number)
    time_3 = timeit.timeit(setup=setup, stmt=stmt[2], number=number)
    time = [time_1, time_2, time_3]
    if time_1 == min(time):
        res = 'loop'
    elif time_2 == min(time):
        res = 'list comprehension'
    elif time_3 == min(time):
        res = 'map'
    
    time = sorted(time)
    print(f'it is better to use a {res}')
    print(f'{time[0]} vs {time[1]} vs {time[2]}')

def check_output():
    emails = 5 * ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com']
    print(loop(emails))
    print(list_comprehension(emails))
    print(list(map_for_list(emails)))

if __name__ == '__main__':
    main()
    check_output()

 