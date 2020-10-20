# Author: gabri
# File: renomear_imagens
# Date: 02/10/2019
# Made with PyCharm

import os


# Function to rename multiple files
def main():
    i = 1
    folder = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(folder, 'downloads/automovel')

    for filename in os.listdir(folder):
        dst = 'carro' + f'{i:04}' + '.jpg'
        src = os.path.join(folder, filename)
        dst = os.path.join(folder, dst)

        # rename() function will
        # rename all the files
        os.rename(src, dst)
        i += 1


# Driver Code
if __name__ == '__main__':
    # Calling main() function
    main()
