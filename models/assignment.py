class Assignment:
    def __init__(self, id, class_id, name, description, due_date, time, assignment_type, completed):
        self.id = id
        self.class_id = class_id
        self.name = name
        self.description = description
        self.due_date = due_date
        self.time = time
        self.assignment_type = assignment_type
        self.completed = completed

    def __key(self):
        return self.id, \
               self.class_id, \
               self.name, \
               self.description, \
               self.due_date, \
               self.time, \
               self.assignment_type, \
               self.completed

    def __eq__(self, other):
        if not isinstance(other, Assignment):
            return NotImplemented
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())
