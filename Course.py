import json


class Course:
    def __init__(self, id, name):
        self.id = id
        self.name = name


def deserialize(response):
    data = json.loads(response)
    courses = []
    for course in data:
        courses.append(Course(course['id'], course['name']))
    return courses
