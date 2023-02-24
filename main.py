from os import path

import dill
import api.setup as setup
from api import caller

file = "data.pkl"

if __name__ == '__main__':
    if path.exists(file):
        with open(file, "rb") as dill_file:
            courses = dill.load(dill_file)

            setup.update(courses)
    else:
        courses = caller.deserialize_courses()

        setup.initialize(courses)

    print("DONE")

    # Save session for persistence
    with open(file, "wb") as dill_file:
        dill.dump(courses, dill_file)
        dill_file.close()
