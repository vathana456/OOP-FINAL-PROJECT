#Menu function for LMS system
from lms import data
from lms.models import Course, Module, ContentItem, Enrollment
from lms.utils.helpers import choose_course, find_enrollment

students = data.students          # List of all students
instructors = data.instructors    # List of all instructors
courses = data.courses            # List of all courses
try:
    enrollments = data.enrollments
except AttributeError:
    enrollments = []

#Instructor Menu
def instructor_menu(teacher):
    # Menu loop for instructor-specific actions
    while True:
        print("\n=== Instructor Menu ===")
        print("1. Create course")
        print("2. Add module + content")
        print("3. View my courses")
        print("4. Logout")

        choice = input("Choose option: ")

        if choice == "1":
            # Instructor creates a new course
            title = input("Course title: ").strip()
            course = teacher.create_course(title)
            courses.append(course)
            print("✅ Course created.")

        elif choice == "2":
            # Add module and content to an existing course
            course = choose_course()
            if not course:
                continue

            module_title = input("Module title: ").strip()
            module_type = input("Module type (e.g., video / quiz / mixed): ").strip().lower()
            module = Module(module_title, content_type=module_type)

            try:
                teacher.add_module(course, module)
            except PermissionError as e:
                print("❌", e)
                continue

            print("Content type examples: video / pdf / ppt / text / link")
            ctype = input("Content type: ").strip().lower()
            ctitle = input("Content title: ").strip()
            cdata = input("Content data (URL/text/filename): ").strip()

            content_item = ContentItem(ctitle, ctype, cdata)

            try:
                module_index = len(course.list_of_modules) - 1
                teacher.add_content(course, module_index, content_item)
            except PermissionError as e:
                print("❌", e)
                continue

            print("✅ Module and content added.")


        elif choice == "3":
            # Show only instructor's courses
            print("\n--- Courses ---")
            found = False
            for c in courses:
                if c.instructor.username == teacher.username:
                    found = True
                    print("-", c.title, "| Modules:", len(c.modules))
            if not found:
                print("No courses created by you yet.")

        elif choice == "4":
            # Exit instructor menu
            break
        else:
            print("Invalid option.")

def student_menu(student):
    # Menu for student actions
    while True:
        print("\n=== Student Menu ===")
        print("1. Enroll in course")
        print("2. Continue learning (next module)")
        print("3. View my progress")
        print("4. Logout")

        choice = input("Choose option: ")
        
        if choice == "1":
            # Enroll student in a selected course
            course = choose_course()
            if not course:
                continue

            if find_enrollment(student, course):
                print("⚠️ Already enrolled in this course.")
                continue

            e = student.enroll(course)
            enrollments.append(e)
            print("✅ Enrolled successfully.")


        elif choice == "2":
            # Continue course by going to next module based on saved progress
            course = choose_course()
            if not course:
                continue

            e = find_enrollment(student, course)
            if not e:
                print("You are not enrolled in this course.")
                continue

            # Get next learning step (module + content) and display it
            try:
                step = student.next_lesson(e)
            except PermissionError as err:
                print("❌", err)
                continue
            if step is None or step == (None, None):
                print("🎉 Course completed!")
                continue

            module, item = step
            print(f"\n📘 Module: {module.title}" + (f" [{module.content_type}]" if getattr(module, "content_type", None) else ""))
            
            if item is None:
                print("  (No content in this module yet)")
            else:
                print("  -", item.content_type.upper(), ":", item.title, "|", item.data)
                
                print("✅ Progress saved:", int(student.progress(e)), "%")

        elif choice == "3":
            # View progress for a selected course
            course = choose_course()
            if not course:
                continue

            e = find_enrollment(student, course)
            if not e:
                print("You are not enrolled in this course.")
                continue

            try:
                pct = student.progress(e)
            except PermissionError as err:
                print("❌", err)
                continue

            print(f"📈 Progress in '{course.title}': {pct:.2f}%")


        elif choice == "4":
            # Exit student menu
            break
        else:
            print("Invalid option.")

