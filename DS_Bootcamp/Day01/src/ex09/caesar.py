import sys

class IncorrectLanguage(Exception):
    pass

class IncorrectCountOfArguments(Exception):
    def __init__(self, count):
        self.count = count
        message = f'Неправильное количесво аргументов - {self.count}'
        super().__init__(message)

def has_cyrillic(text):
    return any('\u0400' <= char <= '\u052F' for char in text)

def encode(text, step):
    answer = ""
    for ch in text:
        if (65 <= ord(ch) <= 90) or (97 <= ord(ch) <= 122):
            number_of_ch = ord(ch)
            if (number_of_ch <= 90) and (number_of_ch + step > 90):
                number_of_ch = 64 + (number_of_ch + step) % 90
            elif (97 <= number_of_ch <= 122) and (number_of_ch + step > 122):
                number_of_ch = 96 + (number_of_ch + step) % 122
            else:
                number_of_ch += step
            answer += chr(number_of_ch)
        else:
            answer += ch

    return answer

def decode(text, step):
    answer = ""
    for ch in text:
        if (65 <= ord(ch) <= 90) or (97 <= ord(ch) <= 122):
            number_of_ch = ord(ch)
            if (number_of_ch <= 90) and (number_of_ch - step < 65):
                number_of_ch = 90 + (number_of_ch - step) - 64
            elif (97 <= number_of_ch <= 122) and (number_of_ch - step < 97):
                number_of_ch = 122 + (number_of_ch - step) - 96
            else:
                number_of_ch -= step
            answer += chr(number_of_ch)
        else:
            answer += ch

    return answer

def caesar():
    arguments = sys.argv

    if (len(arguments) == 4):
        if (has_cyrillic(arguments[2])):
            raise IncorrectLanguage("The script does not support your language yet.")
        elif (arguments[1] == 'encode'):
            answer = encode(arguments[2], int(arguments[3]))
        elif (arguments[1] == 'decode'):
            answer = decode(arguments[2], int(arguments[3]))
        else:
            answer = 'incorrect comand (only encode and decode)'
        
        print(answer)

    else:
        raise IncorrectCountOfArguments(len(arguments))

if __name__ == '__main__':
    caesar()