from os import path

import dill
import api.setup as setup
from api import caller

if __name__ == '__main__':
    if path.exists("coursesPickle.pkl"):
        with open("coursesPickle.pkl", "rb") as dill_file:
            courses = dill.load(dill_file)

            setup.update(courses)
    else:
        courses = caller.deserialize_courses()

        setup.initialize(courses)

    print("DONE")

    # Save session for persistence
    with open("coursesPickle.pkl", "wb") as dill_file:
        dill.dump(courses, dill_file)
        dill_file.close()
