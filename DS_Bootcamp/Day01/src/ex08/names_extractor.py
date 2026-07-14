import sys

def parsing_str(str):
    answer = [""] * 3
    index = 0
    for ch in str:
        if (ch == '.'):
            index += 1
        elif (ch == '@'):
            break
        elif (answer[index] == "") and (index < 2):
            answer[index] += ch.upper()
        else:
            answer[index] += ch.lower()
        answer[2] += ch
    answer[2] += '@corp.com'

    return answer

def write(table):
    f = open('employees.tsv', 'w')
    for line in table:
        for j in range(3):
            f.write(line[j])
            if (j+1 != 3):
                f.write('\t')
            else:
                f.write('\n')
    f.close()

def make_list_of_table(file):
    emails = file.readlines()
    table = []
    for email in emails:
        table.append(parsing_str(email))
    
    return table            

def names_extractor():
    arguments = sys.argv

    if (len(arguments) == 2):
        file = open(arguments[1], 'r')
        if not file.readable():
            print('file cant be read')
        else:
            table = make_list_of_table(file)
            write(table)

if __name__ == '__main__':
    names_extractor()