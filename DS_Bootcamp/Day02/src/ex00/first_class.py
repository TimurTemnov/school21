
class Must_read():
    def __init__(self, path_for_file = 'data.csv'):
        self.path_for_file = path_for_file
    
    def print_file(self):
        file = open(self.path_for_file)
        output = file.read()
        print(output)
    


if __name__ == '__main__':
    exemplar = Must_read()
    exemplar.print_file()
