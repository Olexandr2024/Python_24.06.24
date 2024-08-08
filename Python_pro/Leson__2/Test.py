WWWWD

    def __str__(self):
        students_list = '\n'.join(map(str, self.__students))
        return f'Group: {self.title}\nTeacher: {self.teacher}\nStudents:\n{students_list}'

# Example usage
def main():
    # Create a teacher
    first_name = input('Enter teacher\'s first name: ').strip().title()
    last_name = input('Enter teacher\'s last name: ').strip().title()
    subject = input('Enter subject: ').strip().title()
    teacher = Teacher(first_name, last_name, subject)

    # Create a group
    title = input('Enter group title: ').strip().title()
    group = Group(title, teacher)

    # Add students to the group
    while input('Do you want to add a student? (y/n) ').lower().strip() == 'y':
        first_name = input('Enter student\'s first name: ').strip().title()
        last_name = input('Enter student\'s last name: ').strip().title()
        student = Student(first_name, last_name)
        group.add_student(student)

    print(group)

if __name__ == "__main__":
    main()
