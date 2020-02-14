def avoid(word, forbidden):
    return not any(letter in forbidden for letter in word)

g = (x**2 for x in range(10))
print(next(g))
print(next(g))
print(next(g))
print('inicio loop')

for elem in g:
    print(elem)
    
print(avoid('lol vamos ver', 'kakaka'))
print(avoid('teste som som xd', 'a'))