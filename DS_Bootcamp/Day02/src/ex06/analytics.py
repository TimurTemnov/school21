from random import randint
import os
import logging
import requests
import json

class CantReadFile(Exception):
    pass

class IncorrectForamtOfFile(Exception):
    pass

class ToManyArgumenst(Exception):
    pass

class ReportNotCreate(Exception):
    pass

class Research():
    def __init__(self, path_for_file = 'data.csv'):
        self.path_for_file = path_for_file

        logging.basicConfig(level=logging.INFO, filename='analytics.log', filemode='a', format="%(asctime)s %(message)s")
        logging.info("Initializing a class object Research")

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

        logging.info("Reading data from a file")
        
        return answer_int_list
    
    class Calculations():
        def __init__(self, values):
            self.values = values

            logging.info("Initializing a class object Calculations/Analytics")

        def counts(self):
            orel = 0
            reshka = 0
            for para in self.values:
                if (para[0] == 1):
                    orel += 1
                else:
                    reshka += 1

            logging.info("Calculating the counts of heads and tails")

            return orel, reshka

        def Fractions(self, orel, reshka):

            logging.info("calculating the percentage of heads and tails")

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

            logging.info(f"Prediction of {couunt} events")
            
            return predict_list

        def predict_last(self):
            logging.info("The return of the last event")

            return self.values[-1]
        
        def counts_of_observations(self):
            logging.info("Calculating count of events")

            return len(self.values)

        def save_file(self, data, name_of_file, format_of_file):
            full_filename = name_of_file + '.' + format_of_file

            #if not(os.access(full_filename, os.R_OK)):
            #    raise CantReadFile("Невозможно прочитать файл")
            
            file = open(full_filename, 'w')
            file.write(data)
            file.close()
            logging.info("Writing a report to file")

    def send_message_to_telegram_channel(self, success: bool):
        TOKEN = '8100819426:AAFxD6MWpGEN3g__UNSijVqaW01FmvTDMyQ'
        CHAT_ID = '897214281'

        message = "The report has been successfully created" if success else "The report hasn't been created due to an error"
        
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        params = {
            "chat_id" : CHAT_ID,
            "text" : message
        }

        try:
            response = requests.post(url, json=params)
            logging.info("Message has been send")
            return True
        except Exception as e:
            logging.error(f"Failed to send message")
            return False