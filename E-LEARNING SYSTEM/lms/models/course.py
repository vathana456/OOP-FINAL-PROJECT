class Course:
    # A course belongs to an instructor and contains modules
    def __init__(self, title, instructor):
        self.title = title
        self.instructor = instructor # Instructor object who owns this course
        self.list_of_modules = []  # Internal list to store modules belonging to this course
        self.modules = self.list_of_modules  
        self.index = 0  # Index used for iteration (Iterator Pattern)

    def add_module(self, module):
        # Add a new module to the course
        self.list_of_modules.append(module)

    # Iterator Pattern
    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        # Return the new module in the course
        if self.index < len(self.list_of_modules):
            m = self.list_of_modules[self.index]
            self.index += 1
            return m
        #Stop iteration when all modules are returned
        raise StopIteration

    # Custom iterator: iterate through modules AND their content sequentially
    def content_iterator(self, start_module_index=0, start_content_index=0):
        """Return an iterator that yields (module, content_item) sequentially.
        - If a module has no contents, it yields (module, None) once.
        - start_module_index / start_content_index enable pause/resume.
        """
        return CourseContentIterator(
            course=self,
            start_module_index=start_module_index,
            start_content_index=start_content_index,
        )

    def total_steps(self):
        """Total learning steps (contents, or 1 step for an empty module)."""
        steps = 0
        for m in self.list_of_modules:
            steps += len(getattr(m, "contents", [])) or 1
        return steps


class CourseContentIterator:
    """Iterator over a course's modules + content items in order."""

    def __init__(self, course, start_module_index=0, start_content_index=0):
        self.course = course
        self.module_index = max(0, int(start_module_index))
        self.content_index = max(0, int(start_content_index))

        # Track whether we've already yielded the placeholder for an empty module
        self._yielded_empty_module = False

    def __iter__(self):
        return self

    def __next__(self):
        modules = self.course.list_of_modules

        while self.module_index < len(modules):
            module = modules[self.module_index]
            contents = getattr(module, "contents", []) or []

            # Empty module: yield once (module, None)
            if not contents:
                if not self._yielded_empty_module:
                    self._yielded_empty_module = True
                    self.module_index += 1
                    self.content_index = 0
                    return module, None

                self.module_index += 1
                self.content_index = 0
                self._yielded_empty_module = False
                continue

            # Yield content items in order
            if self.content_index < len(contents):
                item = contents[self.content_index]
                self.content_index += 1

                if self.content_index >= len(contents):
                    self.module_index += 1
                    self.content_index = 0

                return module, item

            self.module_index += 1
            self.content_index = 0

        raise StopIteration


