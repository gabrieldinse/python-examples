import shelve as db

# key e value deve ser str() ou bytes()
database = db.open('resources', 'c') # 'c' cria database se ja n estiver criada
database['gabriel'] = 'dinse'
database['vilma'] = 'dinse'

l = list()

for key in database:
    l.append((str(key), str(database[key])))
    
print(l)
database.close()