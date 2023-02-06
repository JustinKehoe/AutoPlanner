from os import path
from api import caller


if not path.exists("session.pkl"):
    print("herereree")
    courses = caller.deserialize_courses()