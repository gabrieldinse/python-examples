# Author: gabri
# File: Trabalho3
# Date: 25/10/2019
# Made with PyCharm

# Standard Library
import csv
import random

# Third party modules
import numpy as np

# Local application imports


def main():
    with open('data.txt', 'r') as infile, open('shuffled_data.txt', 'w+') as outfile:
        lines = []
        for line in infile:
            lines.append(line)
        random.shuffle(lines)
        outfile.writelines(lines)

    with open('shuffled_data.txt', 'r') as infile, open('commands.txt', 'w+') as outfile:
        reader = csv.reader(infile, delimiter=' ')
        number_of_lines = 0
        all_lines = set()
        for v in reader:
            if int(v[3]) <= 54 and str([v[2], v[3]]) not in all_lines:
                v.extend(['null'] * (8 - len(v)))
                all_lines.add(str([v[2], v[3]]))
                v = ['null' if v[i] == '' else v[i] for i in range(len(v))]
                command = f"INSERT INTO Leituras VALUES ('{v[0]}', {v[2]}, '{v[1]}', {v[4]}, {v[5]}, {v[6]}, {v[7]}, {v[3]});"
                outfile.write(command + '\n')
                number_of_lines += 1
                if number_of_lines == 20000:
                    break


if __name__ == "__main__":
    main()
