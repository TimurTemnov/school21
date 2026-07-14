#!/usr/bin/env python3

import timeit
import random
from collections import Counter

def create_dict(list_of_values):
    answer = {}
    for i in range(1,101):
        count_of_i = 0
        for value in list_of_values:
            if value == i:
                count_of_i += 1
        answer.update({i : count_of_i})
    
    return answer

def top_10(list_of_values):
    my_dict = {}
    for i in range(1,101):
        count_of_i = 0
        for value in list_of_values:
            if value == i:
                count_of_i += 1
        my_dict.update({i : count_of_i})

    sort = sorted(my_dict.items(), key=lambda item: item[1], reverse=True)
    return sort[:10]


def main():
    num_iter = 10
    setup = """
import random
from __main__ import create_dict, top_10
from collections import Counter
list_of_random_values = [random.randint(1,100) for _ in range(1000000)]
"""
    time_1 = timeit.timeit(setup=setup, stmt='create_dict(list_of_random_values)', number=num_iter)
    time_2 = timeit.timeit(setup=setup, stmt='top_10(list_of_random_values)', number=num_iter)
    time_3 = timeit.timeit(setup=setup, stmt='dict(Counter(list_of_random_values))', number=num_iter)
    time_4 = timeit.timeit(setup=setup, stmt='dict(Counter(list_of_random_values).most_common(10))', number=num_iter)

    print(f'my_function: {time_1}')
    print(f'Counter: {time_3}')
    print(f'my top: {time_2}')
    print(f'Counters top: {time_4}')

def check_output():
    list_of_random_values = [random.randint(1,100) for _ in range(1000000)]
    print(f'\n\nmy function: {create_dict(list_of_random_values)} \n\n')
    print(f"Counter: {dict(Counter(list_of_random_values))} \n\n")
    print(f"my top: {top_10(list_of_random_values)}\n\n")
    print(f"Counters top: {dict(Counter(list_of_random_values).most_common(10))}")

if __name__ == '__main__':
    main()
    check_output()
