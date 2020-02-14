class Grade:
    def __init__(self, score, weight):
        self.score = score
        self.weight = weight


class Subject:
    def __init__(self):
        self._grades = []

    def __getitem__(self, index):
        return self._grades[index]

    def __setitem__(self, index, data):
        self._grades[index] = data

    def add_grade(self, score, weight):
        self._grades.append(Grade(score, weight))

    def average_grade(self):
        total_score, total_weight = 0, 0
        for grade in self._grades:
            total_score += grade.score * grade.weight
            total_weight += grade.weight
        return total_score / total_weight


class Student:
    def __init__(self):
        self._subjects = {}

    def __getitem__(self, index):
        return self._subjects[index]

    def __setitem__(self, index, data):
        self._subjects[index] = data

    def add_subject(self, name):
        if name not in self._subjects:
            self._subjects[name] = Subject()
        return self._subjects[name]

    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count


class StudentsList:
    def __init__(self):
        self._students = {}

    def __getitem__(self, index):
        return self._students[index]

    def __setitem__(self, index, data):
        self._students[index] = data

    def add_student(self, name):
        if name not in self._students:
            self._students[name] = Student()
        return self._students[name]


def main():
    students_list = StudentsList()
    name = 'Gabriel Dinse'
    subject = 'Matematica'
    students_list.add_student(name)
    students_list[name].add_subject(subject)
    students_list[name][subject].add_grade(100, 0.1)
    students_list.add_student(name)  # apenas para mostrar que nao interefe
    students_list[name][subject].add_grade(80, 0.2)
    students_list.add_student(name)  # [2]
    students_list[name][subject].add_grade(90, 0.3)
    students_list[name][subject].add_grade(50, 0.3)
    students_list[name][subject].add_grade(60, 0.1)
    print(students_list[name][subject].average_grade())


if __name__ == '__main__':
    main()
