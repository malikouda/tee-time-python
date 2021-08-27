import handlers
from config import Config

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep


def book(args):
    config = Config(**args)

    base_url = "https://magnolia-golf.book.teeitup.com"

    try:
        driver = webdriver.Chrome()
        driver.get(f"{base_url}/login")

        # Log in
        handlers.handle_text_form(
            driver=driver, txtUsername=config.username, txtPassword=config.password
        )

        # Wait for page to load
        WebDriverWait(driver, 10).until(EC.url_contains("course"))

        # Construct new url to set params
        new_url = handlers.construct_url(
            base_url=base_url,
            course=",".join(c.value for c in config.selected_courses),
            date=config.date,
            end=config.end,
            start=config.start,
            min=config.min,
            max=config.max,
            golfers=config.golfers,
            holes=config.holes,
            transportation=config.transportation,
        )

        # Go to the new constructed url with options set
        driver.get(new_url)

        # Wait for tee times to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@data-testid='teetimes-header-date']")
            )
        )

        # Book earliest
        handlers.book_earliest_date(driver=driver)

        # Continue to book
        handlers.continue_to_book(driver=driver)

        # Confirm booking
        handlers.confirm_booking(
            driver=driver,
            full_name=config.full_name,
            phone_number=config.phone_number,
            notes=config.notes,
            testing=config.testing,
        )

        # Make sure reservation was made successfully
        sleep(20)

    except Exception as e:
        print(e)
    finally:
        # Always quit driver
        driver.quit()
