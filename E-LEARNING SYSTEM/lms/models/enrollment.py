# ENROLLMENT (Progress tracking)
class Enrollment:
    """Links a student to a course and tracks progress (pause/resume)."""

    def __init__(self, student, course):
        self.student = student  # Reference to the student object
        self.course = course    # Reference to the course object

        # Cursor into (module_index, content_index)
        self.module_index = 0
        self.content_index = 0

        # Completed steps (for progress %)
        self.steps_completed = 0

        student.enrollments.append(self)

    def next_item(self):
        """Return next learning step as (module, content_item) and advance progress.
        content_item can be None if module has no contents (still counts as 1 step).
        Returns None when finished.
        """
        it = self.course.content_iterator(self.module_index, self.content_index)

        try:
            module, item = next(it)
        except StopIteration:
            return None

        # Save iterator cursor (pause/resume)
        self.module_index = it.module_index
        self.content_index = it.content_index

        self.steps_completed += 1
        return (module, item)

    def progress_percent(self):
        total = self.course.total_steps()
        if total == 0:
            return 0
        return (self.steps_completed / total) * 100
