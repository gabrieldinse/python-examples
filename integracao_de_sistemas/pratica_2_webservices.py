# Author: gabri
# File: pratica_2_webservices
# Date: 29/08/2019
# Made with PyCharm

# Standard Library
import requests
import json

# Third party modules

# Local application imports


def menu_http_request(address, put_path):
    print('\nDeseja efetuar qual operacao? [GET/PUT/QUIT]')
    operation = input('> ')

    if operation == 'GET':
        var = requests.get(address).text
        print('Valor recebido por GET:')
        print(var)
    elif operation == 'PUT':
        data_to_put = {}
        data_to_put['value'] = int(input('Valor: '))
        requests.put(address + put_path, data=data_to_put)
        print('Operacao PUT realizada')
    elif operation == 'QUIT':
        print('\nEncerrando . . .')
        exit(0)
    else:
        print('Operacao errada!')


def main():
    # Em PUT, a variavel data eh enviada no formato x-www-form-urlencoded
    address = "http://localhost:8080/pratica_2_webservices/teste"
    while True:
        menu_http_request(address, '/testeput')


if __name__ == "__main__":
    main()
