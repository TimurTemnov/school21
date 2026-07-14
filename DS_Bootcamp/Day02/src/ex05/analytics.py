from random import randint
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
        def __init__(self, values):
            self.values = values

        def counts(self):
            orel = 0
            reshka = 0
            for para in self.values:
                if (para[0] == 1):
                    orel += 1
                else:
                    reshka += 1

            return orel, reshka

        def Fractions(self, orel, reshka):
            return round(((float(orel) / float(orel + reshka)) * 100),2), round(((float(reshka) / float(orel + reshka)) * 100),2)

    class Analytics(Calculations):
        def predict_random(self, couunt = 3):
            predict_list = []
            for i in range(couunt):
                orel = randint(0,1)
                if (orel == 0):
                    predict_list.append([0,1])
                elif (orel == 1):
                    predict_list.append([1,0])
            
            return predict_list

        def predict_last(self):
            return self.values[-1]
        
        def counts_of_observations(self):
            return len(self.values)

        def save_file(self, data, name_of_file, format_of_file):
            full_filename = name_of_file + '.' + format_of_file
            file = open(full_filename, 'w')
            file.write(data)
            file.close()
