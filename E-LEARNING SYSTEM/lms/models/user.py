# USER CLASSES
from __future__ import annotations
from .course import Course
from .enrollment import Enrollment

class User:
    # Base class for all users (shared fields)
    # Contains common attributes shared by Student and Instructor
    def __init__(self, username, email, password):
        self.username = username   # Unique username used for login and identification
        self.email = email         # Email address of the user
        self.password = password   # User password (stored as plain text for simplicity in this project)

class Student(User):
    # Student class inherits from User
    def __init__(self, username, email, password):
        super().__init__(username, email, password) # Initialize common User attributes
        self.enrollments = []      # list of Enrollment objects
        self.login_count = 0       # Counter to track how many times the student logs in

        def role(self):
            return "student"
 
    # ✅ Student-specific behavior
    def enroll(self, course: Course) -> Enrollment:
        enrollment = Enrollment(self, course)  # Enrollment will attach itself to self.enrollments
        return enrollment

    def next_lesson(self, enrollment: Enrollment):
        if enrollment.student != self:
            raise PermissionError("This enrollment does not belong to this student.")
        return enrollment.next_item()

    def progress(self, enrollment: Enrollment) -> float:
        if enrollment.student != self:
            raise PermissionError("This enrollment does not belong to this student.")
        return enrollment.progress_percent()

class Instructor(User):
    # Instructor inherits from User
    def __init__(self, username, email, password):
        super().__init__(username, email, password)
        self.login_count = 0

        def role(self):
            return "instructor"

    # ✅ Instructor-specific behavior + permissions
    def create_course(self, title: str) -> Course:
        return Course(title=title, instructor=self)

    def add_module(self, course: Course, module):
        if course.instructor != self:
            raise PermissionError("Only the course instructor can add modules.")
        course.add_module(module)

    def add_content(self, course: Course, module_index: int, content_item):
        if course.instructor != self:
            raise PermissionError("Only the course instructor can add content.")
        course.list_of_modules[module_index].add_content(content_item)

