# Author: gabri
# File: 1.13_ordenar_uma_lista_de_dicionarios_por_meio_de_uma_chave_comum
# Date: 28/08/2019
# Made with PyCharm

# Standard Library
from operator import itemgetter

# Third party modules

# Local application imports


def main():
    rows = [
        {'name': 'John', 'lastname': 'Roberts', 'age': 23},
        {'name': 'Ann', 'lastname': 'Vin', 'age': 21},
        {'name': 'David', 'lastname': 'Feyman', 'age': 29},
        {'name': 'Charles', 'lastname': 'Zoomer', 'age': 43}
    ]

    # itemgetter is a callable object
    sorted_by_name = sorted(rows, key=itemgetter('name'))
    sorted_by_age = sorted(rows, key=itemgetter('age'))
    print(sorted_by_name)
    print(sorted_by_age)

    # using itemgetter with min and max
    min_age = min(rows, key=itemgetter('age'))
    max_age = max(rows, key=itemgetter('age'))
    print(min_age)
    print(max_age)


if __name__ == "__main__":
    main()
