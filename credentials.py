import os
from dotenv import load_dotenv


def get_credentials(env_file):
    load_dotenv(env_file)

    email = os.getenv("MAGNOLIA_EMAIL")
    password = os.getenv("MAGNOLIA_PASSWORD")

    return email, password
