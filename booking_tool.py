import handlers
from config import Config

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import logging
from datetime import datetime, time, timedelta
import pause

def book(args):
    booked = False
    try_num = 0
    max_tries = 7

    config = Config(**args)
    base_url = "https://magnolia-golf.book.teeitup.com"

    try:
        chrome_options = Options()
        chrome_options.headless = True
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=chrome_options)
        logging.info("*" * 150)
        logging.info("*" * 150)
        logging.info("Logging in")
        driver.get(f"{base_url}/login")

        logging.info("handle_text_form")
        # Log in
        handlers.handle_text_form(
            driver=driver, txtUsername=config.username, txtPassword=config.password
        )

        logging.info("Wait for initial page to load")
        # Wait for page to load
        WebDriverWait(driver, 100).until(EC.url_contains("course"))

        if config.dont_wait == False:
            logging.info("Waiting for midnight")
            midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1) - timedelta(seconds=1)
            logging.info(f"midnight is {midnight}")
            pause.until(midnight)
            logging.info("It's midnight, let's go")

        for c in config.selected_courses:
            try_num = 0
            if booked:
                break
            logging.info(f"Starting with {c.name}")
            # Construct new url to set params
            new_url = handlers.construct_url(
                base_url=base_url,
                course=c.value,
                date=config.date,
                end=config.end,
                start=config.start,
                min=config.min,
                max=config.max,
                golfers=config.golfers,
                holes=config.holes,
                transportation=config.transportation,
            )

            while not booked and try_num <= max_tries:
                logging.info(f"Trying {c.name} for the {try_num} time")
                try_num += 1
                # Go to the new constructed url with options set
                logging.info(f"Navigating to: {new_url}")
                driver.get(new_url)

                try:
                    found_tee_times = handlers.check_for_tee_times(driver=driver)
                    if found_tee_times:
                        logging.info("found tee times")
                    else:
                        logging.warning(f"No tee times found for loop {try_num}")
                        continue

                    try:
                        # Print tee times found
                        tee_times_found = driver.find_elements_by_css_selector("[data-testid='teetimes-tile-time']")
                        if len(tee_times_found) > 0:
                            logging.info(f"Going to try booking {tee_times_found[0].get_attribute('textContent')}")
                            for t in tee_times_found:
                                logging.info(f"**** {t.get_attribute('textContent')}")
                    except:
                        logging.warning("Error printing list of tee times")

                    # Book earliest
                    handlers.book_earliest_date(driver=driver)
                    logging.info("booked earliest")

                    # Continue to book
                    handlers.continue_to_book(driver=driver, golfers=config.golfers)
                    logging.info("continued to book")

                    # Confirm booking
                    handlers.confirm_booking(
                        driver=driver,
                        full_name=config.full_name,
                        phone_number=config.phone_number,
                        notes=config.notes,
                        testing=config.testing,
                        cc_num=config.cc_num,
                        cc_month=config.cc_month,
                        cc_year=config.cc_year,
                        cc_cvv=config.cc_cvv
                    )
                    logging.info("confirmed booking")
                    if config.testing:
                        back_btn = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    "//button[@data-testid='cancel-and-go-back-btn']",
                                )
                            )
                        )
                        back_btn.click()
                        WebDriverWait(driver, 10).until(EC.url_to_be(f"{base_url}/"))
                        booked = True
                        logging.info("Testing booking complete")
                        sleep(2)
                        continue

                    # Make sure reservation was made successfully
                    logging.info("Wait for confirmation page to load")
                    WebDriverWait(driver, 30).until(EC.url_contains("confirmation"))
                    booked = True
                    logging.info("got to confirmation page")
                except Exception as e:
                    print(e.args)
                    logging.error(e.args)
                    logging.error("error while looking for tee time")
    except Exception as e:
        print(e.args)
        logging.error(e.args)
    finally:
        # Always quit driver
        driver.quit()
