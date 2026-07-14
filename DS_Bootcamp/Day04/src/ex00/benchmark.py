#!/usr/bin/env python3

import timeit

def loop(gmails: list):
    answer_list = []
    for email in gmails:
        if (email.endswith('gmail.com')):
            answer_list.append(email)
    
    return answer_list

def list_comprehension(gmails: list):
    return [email for email in gmails if email.endswith('gmail.com')]

def main():
    setup = """
from __main__ import loop, list_comprehension
emails = 5 * ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com']
"""
        
    stmt_loop = 'loop(emails)'
    stmt_comprehension = 'list_comprehension(emails)'
    number_of_repeats = 90000000

    time_for_loop = timeit.timeit(setup=setup, stmt=stmt_loop, number=number_of_repeats)
    time_for_comprehension = timeit.timeit(setup=setup, stmt=stmt_comprehension, number=number_of_repeats)

    if (time_for_comprehension < time_for_loop):
        print('it is better to use a list comprehension')
        print(f'{time_for_comprehension} vs {time_for_loop}')
    else:
        print('it is better to use a loop')
        print(f'{time_for_loop} vs {time_for_comprehension}')

def check_output():
    emails = 5 * ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com']
    print(loop(emails))
    print(list_comprehension(emails))

if __name__ == '__main__':
    main()