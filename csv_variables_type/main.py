# Author: gabri
# File: main
# Date: 16/06/2019
# Made with PyCharm

# Standard Library
import csv
import ast

# Third party modules
import numpy as np

# Local application imports


def main():
    field_names = ['field1', 'field2', 'field3']
    with open('file.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        writer.writerow(
            {
                field_names[0]: 1,
                field_names[1]: 2,
                field_names[2]: list(
                    np.array([3.3, 4.234, 5.023], dtype=np.float))
            }
        )
        writer.writerow(
            {
                field_names[0]: 100,
                field_names[1]: 200,
                field_names[2]: list(
                    np.array([300.3, 400.234, 500.023], dtype=np.float))
            }
        )

    with open('file.csv', newline='') as file:
        reader = csv.DictReader(file, fieldnames=field_names)
        for row in list(reader)[1:]:
            print(row[field_names[0]],
                  row[field_names[1]],
                  np.array(
                      ast.literal_eval(row[field_names[2]]), dtype=np.float))
            arr = np.array(
                      ast.literal_eval(row[field_names[2]]), dtype=np.float)
            print(arr[0], arr[1], arr[2])


if __name__ == "__main__":
    main()
