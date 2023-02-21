from api import caller


def get_assignments(course):
    assignments = caller.deserialize_assignments(course)

    for assignment in assignments:
        if assignment not in course.assignments:
            course.assignments.append(assignment)
            caller.post_assignment(assignment)


def initialize(courses):
    for course in courses:
        caller.post_course(course)

    update(courses)


def update(courses):
    for course in courses:
        get_assignments(course)
