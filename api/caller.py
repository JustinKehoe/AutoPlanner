import json
import requests
import re

import config
from models.course import Course
from models.assignment import Assignment


def deserialize_courses():
    response = requests.get(config.canvas_api_url + "/courses?enrollment_state=active",
                            headers=config.canvas_api_headers)

    courses_data = json.loads(response.text)

    courses = [Course(course["id"], course["name"]) for course in courses_data
               if course["id"] not in config.blacklisted_courses]

    return courses


def construct_course_body(course):
    return {
        "class": {
            "id": str(course.id),
            "name": course.name,
            "hws": []
        },
        "student": config.myhomework_student_id
    }


def create_courses(courses):
    for course in courses:
        requests.post(config.myhomework_api_url + "/classes",
                      auth=(config.myhomework_client_id, config.myhomework_client_secret),
                      json=construct_course_body(course))

        print(course.name + " has been created")


def sanitize_date(date_value):
    if date_value is not None:
        pattern = re.compile("20[0-9][0-9](-)([0-9][0-9])(-)([0-9][0-9])")

        return re.search(pattern, date_value).group()
    else:
        return ""


def sanitize_time(time_value):
    if time_value is not None:
        pattern = re.compile("[0-9]{2}(:)[0-9]{2}(:)[0-9]{2}")

        sanitized_time = re.search(pattern, time_value).group()

        return sanitized_time + "AM" if int(sanitized_time[0:1]) < 12 else "PM"
    else:
        return ""


def assignment_is_complete(assignment):
    return assignment["workflow_state"] != "unsubmitted"


def deserialize_assignments(course):
    response = requests.get(config.canvas_api_url + "/users/self/courses/" + str(course.id) + "/assignments"
                                                                                              "?include=submission",
                            headers=config.canvas_api_headers)

    assignment_data = json.loads(response.text)

    assignments = [Assignment(assignment["id"],
                              course.id,
                              assignment["name"],
                              assignment["description"],
                              sanitize_date(assignment["due_at"]),
                              sanitize_time(assignment["due_at"]),
                              assignment["submission_types"],
                              assignment_is_complete(assignment["submission"]))
                   for assignment in assignment_data]

    return assignments



def construct_assignment_body(assignment):
    return {
        "hw": {
            "id": str(assignment.id),
            "description": assignment.name,
            "due": assignment.due_date,
            "time": assignment.time,
            "classid": str(assignment.class_id),
            "type": "homework",
            "notes": assignment.description,
            "completed": assignment.completed
        },
        "student": config.myhomework_student_id
    }


def create_assignments(assignments):
    for assignment in assignments:
        requests.post(config.myhomework_api_url + "/homework",
                      auth=(config.myhomework_client_id, config.myhomework_client_secret),
                      json=construct_assignment_body(assignment))

        print(assignment.name + " has been added")
