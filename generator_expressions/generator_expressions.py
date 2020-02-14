line_len = (len(x) for x in open('C:/Users/dell/Google Drive/programas python/Exemplos '
                                 'e testes/generator_expressions/text.txt'))

# line_len  eh  um  iterator  que ao ser percorrido calcula len(posicao atual)
# Isto eh importante para casos de arquivos muito grandes, por exemplo, em que
# nao  se  quer  calcular  imediatamente  todos os valores atraves de uma list
# comprehension
print(next(line_len))
print(next(line_len))
print(next(line_len))

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = (x**2 for x in nums)
square_roots = (x**0.5 for x in squares)
print(next(square_roots))
print(next(square_roots))
print(next(square_roots))
