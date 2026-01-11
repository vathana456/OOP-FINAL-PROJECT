class Module:
    # A module contains learning content
    def __init__(self, title, content_type = None):
        self.title = title                 # module title
        self.content_type = content_type   # video, quiz, etc.
        self.contents = []                 # list of ContentItem objects

    def add_content(self, content_item):
        self.contents.append(content_item)

class ContentItem:
    # Represents a piece of content within a module
    def __init__(self, title, content_type, data):
        self.title = title
        self.content_type = content_type
        self.data = data

