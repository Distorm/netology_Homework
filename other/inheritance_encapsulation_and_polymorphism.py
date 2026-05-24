"""
Практическое задание «ООП: наследование, инкапсуляция и полиморфизм»
    - Задание 1: Наследование и проверка классов
    - Задание 2: Оценки студентов и лекций
    - Задание 3: Сравнение студентов и лекторов
    - Задание 4: Средняя оценка по курсам
"""


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if not isinstance(lecturer, Lecturer):
            return 'Ошибка: можно оценивать только лекторов'
        if course not in self.courses_in_progress:
            return f'Ошибка: студент не записан на курс {course}'
        if course not in lecturer.courses_attached:
            return f'Ошибка: лектор не ведет курс {course}'
        if course in lecturer.grades:
            lecturer.grades[course].append(grade)
        else:
            lecturer.grades[course] = [grade]

    def average_grade(self):
        total = 0
        count = 0
        for grades_list in self.grades.values():
            total += sum(grades_list)
            count += len(grades_list)
        return total / count if count != 0 else 0

    def __str__(self):
        return (
            f"Имя: {self.name} "
            f"Фамилия: {self.surname} "
            f"Средняя оценка за домашние задания: "
            f"{self.average_grade():.2f} "
            f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)} "
            f"Завершенные курсы: {', '.join(self.finished_courses)}"
        )

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() < other.average_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() == other.average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def rate_hw(self, student, course, grade):
        if (
            isinstance(student, Student)
            and course in self.courses_attached
            and course in student.courses_in_progress
        ):
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def average_grade(self):
        total = 0
        count = 0
        for grades_list in self.grades.values():
            total += sum(grades_list)
            count += len(grades_list)
        return total / count if count != 0 else 0

    def __str__(self):
        return (
            f"Имя: {self.name} "
            f"Фамилия: {self.surname} "
            f"Средняя оценка за лекции: {self.average_grade():.2f}"
        )

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() < other.average_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() == other.average_grade()


class Reviewer(Mentor):
    def __str__(self):
        return f"Имя: {self.name} Фамилия: {self.surname}"

def avg_grade_students(students_list, course):
    total = 0
    count = 0
    for student in students_list:
        if course in student.grades:
            total += sum(student.grades[course])
            count += len(student.grades[course])
    return total / count if count != 0 else 0


def avg_grade_lecturers(lecturers_list, course):
    total = 0
    count = 0
    for lecturer in lecturers_list:
        if course in lecturer.grades:
            total += sum(lecturer.grades[course])
            count += len(lecturer.grades[course])
    return total / count if count != 0 else 0


lecturer1 = Lecturer('Иван', 'Иванов')
lecturer2 = Lecturer('Сергей', 'Сергеев')

reviewer1 = Reviewer('Пётр', 'Петров')
reviewer2 = Reviewer('Алексей', 'Алексеев')

student1 = Student('Ольга', 'Алёхина', 'Ж')
student2 = Student('Михаил', 'Иванов', 'М')

# Закрепляем курсы
student1.courses_in_progress += ['Python', 'Java']
student2.courses_in_progress += ['Python', 'C++']

lecturer1.courses_attached += ['Python', 'C++']
lecturer2.courses_attached += ['Java', 'C++']

reviewer1.courses_attached += ['Python', 'C++']
reviewer2.courses_attached += ['Java']

# Reviewer ставит оценки студентам
reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student2, 'Python', 8)
reviewer2.rate_hw(student1, 'Java', 7)
reviewer2.rate_hw(student2, 'C++', 10)

# Student оценивает лектора
student1.rate_lecture(lecturer1, 'Python', 10)
student1.rate_lecture(lecturer2, 'Java', 9)
student2.rate_lecture(lecturer1, 'C++', 8)
student2.rate_lecture(lecturer2, 'C++', 9)


print("\nЗадание 1: Наследование и проверка классов")
print({"lecturer1_is_Mentor": isinstance(lecturer1, Mentor),
        "reviewer1_is_Mentor": isinstance(reviewer1, Mentor)})

print("\nЗадание 2: Оценки студентов и лекций")
print({"student1_grades": student1.grades})
print({"lecturer1_grades": lecturer1.grades})

print("\nЗадание 3: Магические методы __str__")
print({"student1": str(student1)})
print({"lecturer1": str(lecturer1)})
print({"reviewer1": str(reviewer1)})

print("\nЗадание 3: Сравнение студентов и лекторов")
print({"student1 > student2": student1 > student2})
print({"lecturer1 < lecturer2": lecturer1 < lecturer2})

students = [student1, student2]
lecturers = [lecturer1, lecturer2]

print(f"\nЗадание 4: Средняя оценка по курсам")
print({"Средняя оценка студентов по Python":
        avg_grade_students(students, 'Python')})
print({"Средняя оценка студентов по Java":
        avg_grade_students(students, 'Java')})
print({"Средняя оценка лекторов по C++":
        avg_grade_lecturers(lecturers, 'C++')})
print({"Средняя оценка лекторов по Python":
        avg_grade_lecturers(lecturers, 'Python')})
