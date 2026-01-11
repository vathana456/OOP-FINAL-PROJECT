from lms import data

students = data.students
instructors = data.instructors
courses = data.courses
try:
    enrollments = data.enrollments
except AttributeError:
    enrollments = []

# Helper / Utility Functions
def find_student(username):
    # Search student list by username
    # Returns the Student object if found, otherwise None
    for s in students:
        if s.username == username:
            return s
    return None


def find_instructor(username):
    # Search instructor list by username
    # Returns the Instrutor object if found, otherwise None
    for t in instructors:
        if t.username == username:
            return t
    return None


def choose_course():
    # Display all available courses and allow the user to select one
    # Returns the selected Course object or None if selection fails
    if not courses:
        print("No courses available.")
        return None

    print("\n--- Available Courses ---")
    for i, c in enumerate(courses):
        print(i + 1, "-", c.title, "(Teacher:", c.instructor.username + ")")

    try:
        # convert user input to index
        idx = int(input("Choose course number: ")) - 1
    except ValueError:
        print("Invalid input.")
        return None

    # Validate chosen index
    if idx < 0 or idx >= len(courses):
        print("Invalid course number.")
        return None

    return courses[idx]


def find_enrollment(student, course):
    # Find the Enrollment object for this student in this course
    for e in student.enrollments:
        if e.course == course:
            return e
    return None


