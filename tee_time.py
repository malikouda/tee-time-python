import argparse
import logging
import parser_utils
from booking_tool import book

parser = argparse.ArgumentParser(description="Tee time scheduler")

parser.add_argument("--username", required=True, type=str, help="Magnolia username")
parser.add_argument("--password", required=True, type=str, help="Magnolia password")
parser.add_argument(
    "--courses",
    type=parser_utils.handle_courses,
    default=argparse.SUPPRESS,
    nargs="+",
    metavar=["avery_ranch", "teravista", "falconhead"],
    help="Which course(s) to book for",
)
parser.add_argument("--full-name", required=True, type=str, help="Full name")
parser.add_argument(
    "--phone-number",
    required=True,
    type=parser_utils.handle_phone_number,
    help="10-digit phone number",
)
parser.add_argument("--notes", type=str, help="Booking notes")
parser.add_argument(
    "--testing",
    action="store_true",
    help="Do not complete booking (testing purposes only)",
)
parser.add_argument(
    "--date", default=argparse.SUPPRESS, type=str, help="Date to book for"
)
parser.add_argument(
    "--start-hour",
    type=parser_utils.handle_hour,
    help="Start of hours to search for",
)
parser.add_argument(
    "--end-hour", type=parser_utils.handle_hour, help="End of hours to search for"
)
parser.add_argument("--min-price", type=str, help="Min price")
parser.add_argument("--max-price", type=str, help="Max price")
parser.add_argument(
    "--num-golfers",
    required=True,
    type=str,
    choices=list(str(n) for n in range(1, 5)),
    help="Number of golfers",
)
parser.add_argument(
    "--num-holes", type=str, choices=["9", "18"], help="Number of holes"
)
parser.add_argument(
    "--transportation-type",
    type=parser_utils.handle_transportation,
    metavar=["walking", "riding"],
    help="Type of transportation",
)

args = parser.parse_args()

logging.basicConfig(
    filename="teetimes.txt",
    format="%(asctime)s :: %(levelname)s :: %(message)s",
    encoding="utf-8",
    level=logging.INFO,
)

book(vars(args))
