# передлать вывод на интовые значение в массиве

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
    
    def file_reader(self, has_header=True):
        if not(os.access(self.path_for_file, os.R_OK)):
            raise CantReadFile("Невозможно прочитать файл")
        
        file = open(self.path_for_file)        
        
        input_of_file = file.readlines()

        list_input_of_file = []

        if (has_header):
            for line in input_of_file[1:]:
                list_input_of_file.append(line.replace('\n','').split(','))
        else:
            for line in input_of_file:
                list_input_of_file.append(line.replace('\n','').split(','))

        for line in list_input_of_file:
            if ((len(line) == 2) and (line[0] in ('0', '1'))
                and (line[1] in ('0', '1'))
                and (int(line[0]) + int(line[1]) == 1)):
                continue
            else:
                raise IncorrectForamtOfFile("Неккоректный формат файла, некорректные значения параметров")
            
        file.close()

        answer_int_list = []
        for line in list_input_of_file:
            answer_int_list.append([int(line[0]), int(line[1])])
        
        return answer_int_list
    
    class Calculations():
        def counts(self, values):
            orel = 0
            reshka = 0
            for para in values:
                if (para[0] == 1):
                    orel += 1
                else:
                    reshka += 1

            return orel, reshka

        def Fractions(self, orel, reshka):
            return (float(orel) / float(orel + reshka)) * 100, (float(reshka) / float(orel + reshka)) * 100


if __name__ == '__main__':
    argumens = sys.argv

    if len(argumens) == 2:
        exemplar = Research(argumens[1])
        values = exemplar.file_reader()
        orel, reshka = exemplar.Calculations().counts(values)
        frac_orel, frac_reshka = exemplar.Calculations().Fractions(orel, reshka)
        print(values)
        print(orel, reshka)
        print(frac_orel, frac_reshka)
    else:
        raise ToManyArgumenst("Неправлиьное количесвто аргументов, нужно передать только путь до файла")