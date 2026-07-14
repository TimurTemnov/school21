#!/usr/bin/env python3

import timeit
import sys

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

def filter_list(gmails: list):
    return filter(lambda x: x.endswith('gmail.com'), gmails)

def main():
    if len(sys.argv) != 3:
        raise Exception('Wrong number os ARGs')
    name_function = sys.argv[1]
    acceptable_names = ['loop', 'list_comprehension', 'map', 'filter']
    if name_function not in acceptable_names:
        raise Exception('Wrong function name')
    number_of_calls = int(sys.argv[2])
    if number_of_calls < 1:
        raise Exception('Wrong number of calls')
    answer = time_counting(acceptable_names.index(name_function), number_of_calls)
    print(answer)

def time_counting(index_of_method, number_of_calls):
    setup = """
from __main__ import loop, list_comprehension, map_for_list, filter_list
emails = 5 * ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com']
"""
    stmt = ['loop(emails)', 'list_comprehension(emails)', 'map_for_list(emails)', 'filter_list(emails)']

    time = timeit.timeit(setup=setup, stmt=stmt[index_of_method], number=number_of_calls)
    return time
    

def check_output():
    emails = 5 * ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com']
    print(loop(emails))
    print(list_comprehension(emails))
    print(list(map_for_list(emails)))
    print(list(filter_list(emails)))

if __name__ == '__main__':
    main()
    check_output()
