import os

class DifferentFileEncapsulator:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def __enter__(self):
        try:
            with open(self.file_path) as file:
                for line in file:
                    print(line)
        except IOError:
            print('IO Error')
    
    def __exit__(self, type, value, traceback):
        with open(self.file_path, 'w') as file:
            file.write('HAHAHAHHAHAHAHA')

root_path = os.path.dirname(os.path.abspath(__file__))

with DifferentFileEncapsulator(os.path.join(root_path, 'file.txt')):
    pass
