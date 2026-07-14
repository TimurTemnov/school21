def read():
    a = []
    with open('ds.csv') as f:
        a = f.readlines()
    return a

def parsing_by_str(line):
    answer = [""] * 3
    in_chavichki = -1
    index = 0
    for char in line:
        if (char == '\"'):
            answer[index] += char
            in_chavichki *= -1
        elif (char == ',') and (in_chavichki == 1):
            answer[index] += char
        elif (char == ',') and (in_chavichki == -1):
            index += 1
        else:
            answer[index] += char
    return answer

def write(date):
    f = open('ds.tsv', 'w')
    for line in date:
        for j in range(6):
            f.write(line[j])
            if (j+1 != 6):
                f.write('\t')
            else:
                f.write('\n')
    f.close()


def read_and_write():
    data = read()
    pars_date = []
    for line in data:
        pars_date.append(parsing_by_str(line))
    write(pars_date)
    

if __name__ == '__main__':
    read_and_write()