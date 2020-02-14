# Author: gabri
# File: mapping_keys_to_multiples_values
# Date: 28/07/2019
# Made with PyCharm

# Standard Library
from collections import defaultdict

# Third party modules

# Local application imports


def main():
    a = defaultdict(list)
    a['a'].append(1)
    a['a'].append(2)
    a['b'].append(4)
    print(a)


if __name__ == "__main__":
    main()
