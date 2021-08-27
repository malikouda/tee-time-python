from os import getenv
from dotenv import load_dotenv
from courses import Courses
from transportation import Transportation
from datetime import date

load_dotenv("./secrets.env")


class Config:
    # all should be strings
    username = getenv("MAGNOLIA_USERNAME")  # username (set in secrets.env)
    password = getenv("MAGNOLIA_PASSWORD")  # password (set in secrets.env)
    selected_courses = [Courses.avery_ranch, Courses.falconhead]  # courses to look for
    date = str(date.today())  # date
    start = None  # 00 - 23
    end = None  # 00- 23
    min = None  # price
    max = None  # price
    golfers = None  # None - 4 | None means "any"
    holes = None  # None, 9, or 18 | None means 9 or 18
    transportation = None  # walking or riding | None means riding or walking

    # For "confirm booking" page
    full_name = getenv("MAGNOLIA_FULL_NAME") # Full name
    phone_number = getenv("MAGNOLIA_PHONE_NUMBER")  # phone number
    notes = None  # any notes for your reservation
    testing = True  # set this to false to actually make the reservation
