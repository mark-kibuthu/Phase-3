import sys
import os
import click

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.models import get_session, create_database, Student, Teacher, Course

# Initialize the database
@click.command()
def initdb():
    """Initialize the database."""
    engine = get_session().get_bind()
    create_database(engine)
    click.echo("Database initialized!")

# CRUD operations

def add_student():
    session = get_session()
    name = click.prompt("Enter student name")
    major = click.prompt("Enter student major")
    year = click.prompt("Enter student year", type=int)

    student = Student(name=name, major=major, year=year)
    session.add(student)
    session.commit()
    click.echo(f"Student {name} added!")

def add_teacher():
    session = get_session()
    name = click.prompt("Enter teacher name")
    department = click.prompt("Enter teacher department")

    teacher = Teacher(name=name, department=department)
    session.add(teacher)
    session.commit()
    click.echo(f"Teacher {name} added!")

def add_course():
    session = get_session()
    
    name = input("Enter course name: ")
    credits = input("Enter number of credits: ")
    
    try:
        credits = int(credits)
    except ValueError:
        print("Credits must be an integer.")
        return
    
    teachers = session.query(Teacher).all()
    if not teachers:
        print("No teachers available. Please add a teacher first.")
        return
    
    print("Available teachers:")
    for teacher in teachers:
        print(f"{teacher.id}: {teacher.name} (Department: {teacher.department})")
    
    teacher_id = input("Enter teacher ID for the course: ")
    
    try:
        teacher_id = int(teacher_id)
    except ValueError:
        print("Invalid teacher ID.")
        return
    
    teacher = session.query(Teacher).filter_by(id=teacher_id).first()
    if not teacher:
        print("Teacher ID not found.")
        return
    
    new_course = Course(name=name, credits=credits, teacher_id=teacher_id)
    session.add(new_course)
    session.commit()
    
    print(f"Course '{name}' added successfully.")

def update_student():
    session = get_session()
    
    students = session.query(Student).all()
    if not students:
        print("No students found.")
        return
    
    print("Available students:")
    for student in students:
        print(f"{student.id}: {student.name} (Major: {student.major}, Year: {student.year})")
    
    student_id = input("Enter the ID of the student to update: ")
    
    try:
        student_id = int(student_id)
    except ValueError:
        print("Invalid student ID.")
        return
    
    student = session.query(Student).filter_by(id=student_id).first()
    if not student:
        print("Student ID not found.")
        return
    
    name = input(f"Enter new name for student (current: {student.name}): ")
    major = input(f"Enter new major for student (current: {student.major}): ")
    year = input(f"Enter new year for student (current: {student.year}): ")
    
    student.name = name or student.name
    student.major = major or student.major
    student.year = year or student.year
    
    session.commit()
    
    print(f"Student {student_id} updated successfully.")

def update_teacher():
    session = get_session()
    
    teachers = session.query(Teacher).all()
    if not teachers:
        print("No teachers found.")
        return
    
    print("Available teachers:")
    for teacher in teachers:
        print(f"{teacher.id}: {teacher.name} (Department: {teacher.department})")
    
    teacher_id = input("Enter the ID of the teacher to update: ")
    
    try:
        teacher_id = int(teacher_id)
    except ValueError:
        print("Invalid teacher ID.")
        return
    
    teacher = session.query(Teacher).filter_by(id=teacher_id).first()
    if not teacher:
        print("Teacher ID not found.")
        return
    
    name = input(f"Enter new name for teacher (current: {teacher.name}): ")
    department = input(f"Enter new department for teacher (current: {teacher.department}): ")
    
    teacher.name = name or teacher.name
    teacher.department = department or teacher.department
    
    session.commit()
    
    print(f"Teacher {teacher_id} updated successfully.")

def update_course():
    session = get_session()
    
    courses = session.query(Course).all()
    if not courses:
        print("No courses found.")
        return
    
    print("Available courses:")
    for course in courses:
        print(f"{course.id}: {course.name} (Credits: {course.credits})")
    
    course_id = input("Enter the ID of the course to update: ")
    
    try:
        course_id = int(course_id)
    except ValueError:
        print("Invalid course ID.")
        return
    
    course = session.query(Course).filter_by(id=course_id).first()
    if not course:
        print("Course ID not found.")
        return
    
    name = input(f"Enter new name for course (current: {course.name}): ")
    credits = input(f"Enter new credits for course (current: {course.credits}): ")
    
    if credits:
        try:
            credits = int(credits)
        except ValueError:
            print("Credits must be an integer.")
            return
    
    course.name = name or course.name
    course.credits = credits if credits is not None else course.credits
    
    session.commit()
    
    print(f"Course {course_id} updated successfully.")

def delete_student():
    session = get_session()
    
    students = session.query(Student).all()
    if not students:
        print("No students found.")
        return
    
    print("Available students:")
    for student in students:
        print(f"{student.id}: {student.name} (Major: {student.major}, Year: {student.year})")
    
    student_id = input("Enter the ID of the student to delete: ")
    
    try:
        student_id = int(student_id)
    except ValueError:
        print("Invalid student ID.")
        return
    
    student = session.query(Student).filter_by(id=student_id).first()
    if not student:
        print("Student ID not found.")
        return
    
    session.delete(student)
    session.commit()
    
    print(f"Student {student_id} deleted successfully.")

def delete_teacher():
    session = get_session()
    
    teachers = session.query(Teacher).all()
    if not teachers:
        print("No teachers found.")
        return
    
    print("Available teachers:")
    for teacher in teachers:
        print(f"{teacher.id}: {teacher.name} (Department: {teacher.department})")
    
    teacher_id = input("Enter the ID of the teacher to delete: ")
    
    try:
        teacher_id = int(teacher_id)
    except ValueError:
        print("Invalid teacher ID.")
        return
    
    teacher = session.query(Teacher).filter_by(id=teacher_id).first()
    if not teacher:
        print("Teacher ID not found.")
        return
    
    session.delete(teacher)
    session.commit()
    
    print(f"Teacher {teacher_id} deleted successfully.")

def delete_course():
    session = get_session()
    
    courses = session.query(Course).all()
    if not courses:
        print("No courses found.")
        return
    
    print("Available courses:")
    for course in courses:
        print(f"{course.id}: {course.name} (Credits: {course.credits})")
    
    course_id = input("Enter the ID of the course to delete: ")
    
    try:
        course_id = int(course_id)
    except ValueError:
        print("Invalid course ID.")
        return
    
    course = session.query(Course).filter_by(id=course_id).first()
    if not course:
        print("Course ID not found.")
        return
    
    session.delete(course)
    session.commit()
    
    print(f"Course {course_id} deleted successfully.")

def view_students():
    session = get_session()
    
    students = session.query(Student).all()
    if not students:
        print("No students found.")
        return
    
    print("Students:")
    for student in students:
        print(f"ID: {student.id}, Name: {student.name}, Major: {student.major}, Year: {student.year}")

def view_teachers():
    session = get_session()
    
    teachers = session.query(Teacher).all()
    if not teachers:
        print("No teachers found.")
        return
    
    print("Teachers:")
    for teacher in teachers:
        print(f"ID: {teacher.id}, Name: {teacher.name}, Department: {teacher.department}")

def view_courses():
    session = get_session()
    
    courses = session.query(Course).all()
    if not courses:
        print("No courses found.")
        return
    
    print("Courses:")
    for course in courses:
        print(f"ID: {course.id}, Name: {course.name}, Credits: {course.credits}")

def enroll_student():
    session = get_session()
    
    students = session.query(Student).all()
    if not students:
        print("No students found.")
        return
    
    print("Available students:")
    for student in students:
        print(f"{student.id}: {student.name}")
    
    student_id = input("Enter student ID to enroll: ")
    
    try:
        student_id = int(student_id)
    except ValueError:
        print("Invalid student ID.")
        return
    
    student = session.query(Student).filter_by(id=student_id).first()
    if not student:
        print("Student ID not found.")
        return
    
    courses = session.query(Course).all()
    if not courses:
        print("No courses available to enroll.")
        return
    
    print("Available courses:")
    for course in courses:
        print(f"{course.id}: {course.name} (Credits: {course.credits})")
    
    course_id = input("Enter course ID to enroll in: ")
    
    try:
        course_id = int(course_id)
    except ValueError:
        print("Invalid course ID.")
        return
    
    course = session.query(Course).filter_by(id=course_id).first()
    if not course:
        print("Course ID not found.")
        return
    
    student.courses.append(course)
    session.commit()
    
    print(f"Student {student.name} enrolled in course {course.name}.")

# Main menu function
def menu():
    while True:
        click.echo("\nMain Menu:")
        click.echo("1. Add Student")
        click.echo("2. Add Teacher")
        click.echo("3. Add Course")
        click.echo("4. Update Student")
        click.echo("5. Update Teacher")
        click.echo("6. Update Course")
        click.echo("7. Delete Student")
        click.echo("8. Delete Teacher")
        click.echo("9. Delete Course")
        click.echo("10. View Students")
        click.echo("11. View Teachers")
        click.echo("12. View Courses")
        click.echo("13. Enroll Student in Course")
        click.echo("14. Initialize Database")
        click.echo("15. Exit")
        
        choice = click.prompt("Enter your choice", type=int)
        
        if choice == 1:
            add_student()
        elif choice == 2:
            add_teacher()
        elif choice == 3:
            add_course()
        elif choice == 4:
            update_student()
        elif choice == 5:
            update_teacher()
        elif choice == 6:
            update_course()
        elif choice == 7:
            delete_student()
        elif choice == 8:
            delete_teacher()
        elif choice == 9:
            delete_course()
        elif choice == 10:
            view_students()
        elif choice == 11:
            view_teachers()
        elif choice == 12:
            view_courses()
        elif choice == 13:
            enroll_student()
        elif choice == 14:
            initdb()
        elif choice == 15:
            click.echo("Exiting...")
            break
        else:
            click.echo("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
