import json
import requests

import config
from models.course import Course

# Courses which don't have an end date in Canvas
blacklisted_courses = ["N2npDCFcWxWNii2EFsPQntEFcy22KWb8BZg88O8M", "gv4v9rYzMaj5OTkExucEP8LHAqIAmMBxJcGBLLgC"]


def deserialize_courses():
    response = requests.get(config.canvas_api_url + "/courses?enrollment_state=active",
                            headers=config.canvas_api_headers)

    courses_data = json.loads(response.text)

    courses = [Course(course['uuid'], course['name']) for course in courses_data
               if course['uuid'] not in blacklisted_courses]

    return courses


def construct_course_body(course):
    return {
        "class": {
            "id": course.id,
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

