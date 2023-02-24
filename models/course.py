import config


class Course:
    def __init__(self, id, name):
        self.id = id
        self.name = name

        self.assignments = []

    def construct_course_body(self):
        return {
            "class": {
                "id": str(self.id),
                "name": self.name,
                "hws": []
            },
            "student": config.myhomework_student_id
        }