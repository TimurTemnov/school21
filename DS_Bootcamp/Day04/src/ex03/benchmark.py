#!/usr/bin/env python3

import timeit
import sys
from functools import reduce

def func_loop(iterable):
    sum = 0
    for i in iterable:
        sum += i*i
    return sum

def func_reduce(iterable):
    return reduce(lambda x,y: x + y*y, iterable)

def main():
    if len(sys.argv) != 4:
        raise Exception('Wrong number of arguments, must be 4 args')

    acceptable_names = ['loop', 'reduce']
    name_of_function = sys.argv[1]
    if name_of_function not in acceptable_names:
        raise Exception('Wrong name of function, must be loop or reduce')

    number_of_calls = int(sys.argv[2])
    number_of_sum = int(sys.argv[3])
    if (number_of_calls < 1) or (number_of_sum < 1):
        raise Exception('Wrong naumber of calls or number of sum, must be > 0') 
    
    answer = time_counting(name_of_function, number_of_calls, number_of_sum)
    print(answer)

def time_counting(name_of_method, number_of_calls, number_of_sum):
    setup = """
from __main__ import func_loop, func_reduce
"""  
    stmt = f'func_{name_of_method}({range(1,number_of_sum+1)})'
    time = timeit.timeit(setup=setup, stmt=stmt,number=number_of_calls)
    return time

def check_output(number_of_sum):
    print(func_loop(number_of_sum))
    print(func_reduce(number_of_sum))


if __name__ == '__main__':
    main()
    check_output(range(1,8))
