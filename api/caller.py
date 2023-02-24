import json
import requests

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


def post_course(course):
    requests.post(config.myhomework_api_url + "/classes",
                  auth=(config.myhomework_client_id, config.myhomework_client_secret),
                  json=course.construct_course_body())

    print(course.name + " has been created")


def deserialize_assignments(course):
    response = requests.get(config.canvas_api_url + "/users/self/courses/" + str(course.id) + "/assignments"
                                                                                              "?include=submission",
                            headers=config.canvas_api_headers)

    assignment_data = json.loads(response.text)

    assignments = [Assignment(assignment["id"],
                              course.id,
                              assignment["name"],
                              assignment["description"],
                              Assignment.sanitize_date(assignment["due_at"]),
                              Assignment.sanitize_time(assignment["due_at"]),
                              assignment["submission_types"],
                              Assignment.is_complete(assignment["submission"]))
                   for assignment in assignment_data]

    return assignments


def post_assignment(assignment):
    requests.post(config.myhomework_api_url + "/homework",
                  auth=(config.myhomework_client_id, config.myhomework_client_secret),
                  json=Assignment.construct_assignment_body(assignment))

    print(assignment.name + " has been posted")
