from courses import Courses
from transportation import Transportation


def handle_phone_number(num):
    num = num.replace(" ", "")
    return f"+1 ({num[:3]}) {num[3:6]}-{num[6:]}"


def handle_courses(*courses):
    new = []
    for course in courses:
        new.append(getattr(Courses, course))
    return new


def handle_hour(num):
    return str(num).zfill(2)


def handle_transportation(transportation_type):
    return getattr(Transportation, transportation_type).value
