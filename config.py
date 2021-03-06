from datetime import datetime
from courses import Courses
from datetime import timedelta


class Config:
    def __init__(
        self,
        username=None,
        password=None,
        courses=[Courses.avery_ranch, Courses.falconhead],
        full_name=None,
        phone_number=None,
        testing=True,
        date=str(datetime.now() + timedelta(days=10, hours=3))[:10],
        notes=None,
        start_hour=None,
        end_hour=None,
        min_price=None,
        max_price=None,
        num_golfers=None,
        num_holes=None,
        transportation_type=None,
    ):
        self.username = username
        self.password = password
        self.selected_courses = courses
        self.full_name = full_name
        self.phone_number = phone_number
        self.notes = notes
        self.testing = testing
        self.date = date
        self.start = start_hour
        self.end = end_hour
        self.min = min_price
        self.max = max_price
        self.golfers = num_golfers
        self.holes = num_holes
        self.transportation = transportation_type
