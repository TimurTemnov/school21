import sys

def find_name(email):
    f = open('employees.tsv')
    date = f.readlines()
    table = []
    index = 0
    for line in date:
        table.append(line.split('\t'))
        table[index][2] = table[index][2][:-1]
        index += 1

    name = ""
    for i in range(len(table)):
        if (email == table[i][2]):
            name = table[i][0]

    return name

def letter_starter():
    arguments = sys.argv

    if (len(arguments) == 2):
        name = find_name(arguments[1])
        if not(name == ""):
            print(f"Dear {name}, welcome to our team. We are sure that it will be a pleasure to work with you. That’s a precondition for the professionals that our company hires.")

if __name__ == '__main__':
    letter_starter()