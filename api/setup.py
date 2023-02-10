from os import path
from api import caller


if not path.exists("session.pkl"):
    courses = caller.deserialize_courses()

    caller.create_courses(courses)

    for course in courses:
        course.homework = caller.deserialize_assignments(course)

        caller.create_assignments(course.homework)

