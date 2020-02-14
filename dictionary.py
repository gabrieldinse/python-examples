def histogram(str):
    hist = {}
    for c in str:
        hist[c] = hist.get(c, 0) + 1
    return hist

def printDictionary(dictionary):
    for i in dictionary:
        print(i, dictionary[i])

str = 'banana e morango'
hist = histogram(str)
print('String: ' + str)
printDictionary(hist)