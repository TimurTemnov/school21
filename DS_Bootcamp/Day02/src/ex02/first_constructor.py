import sys
import os

class CantReadFile(Exception):
    pass

class IncorrectForamtOfFile(Exception):
    pass

class ToManyArgumenst(Exception):
    pass

class Research():
    def __init__(self, path_for_file = 'data.csv'):
        self.path_for_file = path_for_file
    
    def file_reader(self):
        if not(os.access(self.path_for_file, os.R_OK)):
            raise CantReadFile("Невозможно прочитать файл")
        
        file = open(self.path_for_file)        
        
        input_of_file = file.readlines()

        check_input = []
        for line in input_of_file:
            check_input.append(line.replace('\n','').split(','))

        if (len(check_input[0]) != 2):
            raise IncorrectForamtOfFile("Некорректный формат файла, некорректный заголовок")
        for line in check_input[1:]:
            if ((len(line) == 2) and (line[0] in ('0', '1'))
                and (line[1] in ('0', '1'))
                and (int(line[0]) + int(line[1]) == 1)):
                continue
            else:
                raise IncorrectForamtOfFile("Неккоректный формат файла, некорректные значения параметров")
            
        file.close()
        
        return input_of_file
    


if __name__ == '__main__':
    argumens = sys.argv

    if len(argumens) == 2:
        exemplar = Research(argumens[1])
        text = exemplar.file_reader()
        for line in text:
            print(line, end='')
        print('')
    else:
        raise ToManyArgumenst("Неправлиьное количесвто аргументов, нужно передать только путь до файла")