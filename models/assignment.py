from dateutil import parser
import pytz
import config


class Assignment:
    def __init__(self, id, class_id, name, description, due_date, time, assignment_type, completed):
        self.id = id
        self.class_id = class_id
        self.name = name
        self.description = description
        self.due_date = due_date
        self.time = time
        self.assignment_type = assignment_type
        self.completed = completed

    def __key(self):
        return self.id, \
               self.class_id, \
               self.name, \
               self.description, \
               self.due_date, \
               self.time, \
               self.assignment_type, \
               self.completed

    @staticmethod
    def sanitize_date(date_value):
        if date_value is not None:
            return str(parser.isoparse(date_value).astimezone(tz=pytz.timezone(config.local_timezone)).date())
        else:
            return ""

    @staticmethod
    def sanitize_time(time_value):
        if time_value is not None:
            return str(parser.isoparse(time_value).astimezone(tz=pytz.timezone(config.local_timezone)).astimezone(
                tz=pytz.timezone(config.local_timezone)).time().strftime("%I:%M:%S %p"))
        else:
            return ""

    @staticmethod
    def is_complete(assignment_state):
        return assignment_state["workflow_state"] != "unsubmitted"

    def construct_assignment_body(self):
        return {
            "hw": {
                "id": str(self.id),
                "description": self.name,
                "due": self.due_date,
                "time": self.time,
                "classid": str(self.class_id),
                "type": "homework",
                "notes": self.description,
                "completed": self.completed
            },
            "student": config.myhomework_student_id
        }

    def __eq__(self, other):
        if not isinstance(other, Assignment):
            return NotImplemented
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())