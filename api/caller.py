import json
import requests

import config
from models.course import Course

blacklisted_courses = [146020000000016677, 146020000000012047]  # Courses which don't have an end date in Canvas


def deserialize_courses():
    response = requests.get(config.canvas_api_url,
                            headers=config.canvas_api_headers)

    courses_data = json.loads(response.text)

    courses = [Course(course['id'], course['name']) for course in courses_data
               if course['id'] not in blacklisted_courses]

    return courses
