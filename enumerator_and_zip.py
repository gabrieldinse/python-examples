l = ['abacaxi', 'banana', 'cenoura', 'damasco', 'equador', 'fraco']
for i, elem in enumerate(l):
    print('%d: %s' % (i, elem))
    
lens = [len(x) for x in l]

for i, elem in zip(lens, l):
    print('%s: %d letra(s)' % (elem, i))
