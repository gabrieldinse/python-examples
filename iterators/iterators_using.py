class ReadVisits(object):
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)


def normalize_defensive(numbers):
    if iter(numbers) is iter(numbers):
        raise TypeError('Must supply a container')

    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)

    return result


path = 'text.txt'
visits = [15, 35, 80]
print(normalize_defensive(visits))  # No error
visits = ReadVisits(path)  # 'iter(ReadVisits(path))' nao funcionaria
print(normalize_defensive(visits))  # No error
