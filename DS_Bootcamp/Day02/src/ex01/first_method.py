
class Research():
    def __init__(self, path_for_file = 'data.csv'):
        self.path_for_file = path_for_file
    
    def file_reader(self):
        file = open(self.path_for_file)
        output = file.read()
        return output
    


if __name__ == '__main__':
    exemplar = Research()
    print(exemplar.file_reader())
