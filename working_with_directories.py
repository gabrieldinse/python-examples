import os

directory = os.path.abspath(os.curdir)

def walk(dirname):
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name) # junta 'caminho' + 'nome do arquivo'
        if os.path.isfile(path):
            print(path + '\n')
        else:
            walk(path)

walk(directory)