def exceptTest(num):
    print('numero de entrada: %d' % (num))

    try:
        # geralmente aqui vai a abertura de arquivos, operacoes matematicas ou
        # de indices de estruturas de imagens que podem gerar exceptions
        print('> bloco try: executa codigo que pode gerar exception')
        if (num > 100):
            # verificar possiveis exceptions que podem ser geradas no programa
            # por pelas bibliotecas utlizadas
            raise ZeroDivisionError
    except ZeroDivisionError as e:
        # propaga a exception ou termina o programa e faz alguns ajustes nos
        # imagens que falharam, se necessario
        print('> bloco except: exception foi gerada no bloco try')
    else:
        # exception nao foi gerada, continua com as operacoes normalmente. Se
        # operacoes aqui podem gerar exception pode-se criar um novo bloco try
        # aninhado a este, ou fazer o except pegar todas as exceptions possiveis
        # no primeiro try
        print('> bloco else: exception nao foi gerada no bloco try')
        return 1
    finally:
        # sempre executa (geralmente fechamento de arquivos), mesmo que o bloco
        # else ja tenha executado (um retorno da funcao, por exemplo)
        print('> bloco finally: executa sempre no final, independente do'
              ' que acontecer antes')


print('se numero > 100 levanta uma exception\n')
exceptTest(int(input('digite o numero: ')))

