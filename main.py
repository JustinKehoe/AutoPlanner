import requests
import config

import Course

if __name__ == '__main__':
    json_string = requests.get(config.canvas_api_url, headers=config.canvas_api_headers).text
    courses = Course.deserialize(json_string)

    for course in courses:
        print(course.id)
        print(course.name)
