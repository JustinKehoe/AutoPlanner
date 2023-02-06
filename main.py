import dill
from api import caller, setup

if __name__ == '__main__':
    dill.load_module("session.pkl")
    print(globals().items())

    for course in setup.courses:
        print(course.id)
        print(course.name)

    # Save session for persistence
    dill.dump_module('session.pkl')
