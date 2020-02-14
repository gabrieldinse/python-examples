from ecommerce.products import Product
from ecommerce.payments.square import Square
from ecommerce.database import DataBase as DB


def main():
    a = Product()
    b = Square()
    c = DB()
    print('ok!')


if __name__ == '__main__':
    main()
