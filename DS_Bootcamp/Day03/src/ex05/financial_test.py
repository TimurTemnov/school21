import pytest
from  financial import parse

def test_tuple():
    result = parse('MSFT', 'Total Revenue')
    assert type(result) is tuple

def test_total_rev():
    result = parse('MSFT', 'Total Revenue')
    assert result[0] == 'Total Revenue'
    assert result[1] == '270,010,000 '

def test_exception_for_ticks():
    with pytest.raises(Exception):
        parse('asdf', 'Total Revenue')
    
def test_exception_for_field():
    with pytest.raises(Exception):
        parse('MSFT', 'lkjh')

def test_exception_for_args_0():
    with pytest.raises(Exception):
        parse()

def test_exception_for_args_1():
    with pytest.raises(Exception):
        parse('MSFT')


if __name__ == '__main__':
    test_total_rev()
    test_total_rev()
    test_exception_for_args_0()
    test_exception_for_args_1()
    test_exception_for_field()
    test_exception_for_ticks()

# pytest financial_test.py