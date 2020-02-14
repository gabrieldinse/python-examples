def force_keyword_arguments(var1, var2, *, karg1=False, karg2=False):
    print('ok!')


# argumentos apos '*' devem ser especificados (caso queira) apenas usando
# sua keyword

# exemplo:
# force_keyword_arguments(1, 2.34, True) # errado!
force_keyword_arguments(1, 2.34, karg2=True, karg1=True)  # ok!
force_keyword_arguments('abacaxi', 2.34, karg2=True)  # ok!
# force_keyword_arguments('a', 'lol', karg1=True, False)  # errado!
