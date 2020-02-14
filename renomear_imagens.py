# Author: gabri
# File: renomear_imagens
# Date: 02/10/2019
# Made with PyCharm

import os


# Function to rename multiple files
def main():
    i = 32
    folder = "C:\\Users\\gabri\\Downloads\\fotos"

    for filename in os.listdir(folder):
        if 'montagem_base' in filename:
            dst = 'montagem_base_plataforma_' + f'{i}' + '.jpeg'
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
