from os import path
from api import caller


if not path.exists("session.pkl"):
    courses = caller.deserialize_courses()

    caller.create_courses(courses)
