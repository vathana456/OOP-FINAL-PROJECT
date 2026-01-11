# (Imports added for package structure)
from lms import data
from lms.models import Student, Instructor
from lms.utils.helpers import find_student, find_instructor
from lms.cli.menus import instructor_menu, student_menu

students = data.students          # List of all students
instructors = data.instructors    # List of all instructors
courses = data.courses            # List of all courses

# Enrollment list may not exist in some versions, so we handle it safely
try:
    enrollments = data.enrollments
except AttributeError:
    enrollments = []

# User Registration Function
def register():
    # Create a new student or instructor
    print("\n=== Registration ===")
    print("1. Student")
    print("2. Instructor")
    role = input("Choose role: ")

    # Collect user credentials
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()

    if role == "1":
        # Prevent duplicate student usernames
        if find_student(username):
            print("Student username already exists.")
            return
        students.append(Student(username, email, password))
        print("✅ Student registered.")

    elif role == "2":
        # Prevent duplicate instructor usernames
        if find_instructor(username):
            print("Instructor username already exists.")
            return
        instructors.append(Instructor(username, email, password))
        print("✅ Instructor registered.")
    else:
        print("Invalid role.")


# Login Function
def login():
    # Login as student or instructor by checking username + password
    print("\n=== Login ===")
    print("1. Student")
    print("2. Instructor")
    role = input("Choose role: ")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if role == "1":
        s = find_student(username)
        if s and s.password == password:
            s.login_count += 1  # record login
            print("✅ Login successful (Student).")
            return "student", s

    elif role == "2":
        t = find_instructor(username)
        if t and t.password == password:
            t.login_count += 1  # record login
            print("✅ Login successful (Instructor).")
            return "instructor", t
    # Login failed
    print("❌ Login failed.")
    return None, None

# Main Program Loop
def main():
    # Main menu loop for the LMS system
    while True:
        print("\n========== LMS MAIN MENU ==========")
        print("I. Register")
        print("II. Login")
        print("III. View all courses")
        print("IV. Exit")

        choice = input("Choose option: ")

        if choice == "I":
            # Create new user
            register()

        elif choice == "II":
            # Login and redirect to role menu
            role, user = login()
            if role == "student":
                student_menu(user)
            elif role == "instructor":
                instructor_menu(user)

        elif choice == "III":
            # Display all available courses in the system
            if not courses:
                print("No courses available.")
            else:
                print("\n--- All Courses ---")
                for c in courses:
                    print("-", c.title, "(Teacher:", c.instructor.username + ")", "| Modules:", len(c.modules))

        elif choice == "IV":
            # Exit the application
            print("Goodbye!")
            break

        else:
            print("Invalid option.")

