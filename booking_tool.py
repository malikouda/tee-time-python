import handlers
from config import Config

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import logging

def book(args):
    logging.basicConfig(filename='teetimes.txt',
                        format='%(asctime)s :: %(levelname)s :: %(message)s',
                        encoding='utf-8', level=logging.INFO)
    booked = False
    try_num = 0
    max_tries = 10

    config = Config(**args)
    base_url = "https://magnolia-golf.book.teeitup.com"

    try:
        chrome_options = Options()
        chrome_options.headless = True
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        logging.info('*'*150)
        logging.info('*'*150)
        logging.info('Logging in')
        driver.get(f"{base_url}/login")

        logging.info('handle_text_form')
        # Log in
        handlers.handle_text_form(
            driver=driver, txtUsername=config.username, txtPassword=config.password
        )

        logging.info('Wait for initial page to load')
        # Wait for page to load
        WebDriverWait(driver, 100).until(EC.url_contains("course"))

        for c in config.selected_courses:
            try_num = 0
            if booked:
                break
            logging.info(f'Starting with {c.name}')
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
                logging.info(f'Trying {c.name} for the {try_num} time')
                try_num += 1
                # Go to the new constructed url with options set
                logging.info(f'Navigating to: {new_url}')
                driver.get(new_url)

                try:
                    # First check to see if there are no tee times
                    no_tee_times = None
                    try:
                        no_tee_times = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located(
                                (By.XPATH,
                                 "//*[@data-testid='no-tee-times-found']")
                            )
                        )
                    except Exception as e:
                        logging.error(e.args)
                        logging.error('assuming we found some tee times')
                    if no_tee_times:
                        logging.warning(f'No tee times found for loop {try_num}')
                        continue

                    # Wait for tee times to load
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                             "//*[@data-testid='teetimes-header-date']")
                        )
                    )
                    logging.info('found tee times')

                    # Book earliest
                    handlers.book_earliest_date(driver=driver)
                    logging.info('booked earliest')

                    # Continue to book
                    handlers.continue_to_book(driver=driver,golfers=config.golfers)
                    logging.info('continued to book')

                    # Confirm booking
                    handlers.confirm_booking(
                        driver=driver,
                        full_name=config.full_name,
                        phone_number=config.phone_number,
                        notes=config.notes,
                        testing=config.testing,
                    )
                    logging.info('confirmed booking')
                    if config.testing:
                        booked = True
                        logging.info('Testing booking complete')
                        sleep(2)
                        continue

                    # Make sure reservation was made successfully
                    logging.info('Wait for confirmation page to load')
                    WebDriverWait(driver, 30).until(EC.url_contains("confirmation"))
                    booked = True
                    logging.info('got to confirmation page')
                except Exception as e:
                    print(e.args)
                    logging.error(e.args)
                    logging.error('error while looking for tee time')
    except Exception as e:
        print(e.args)
        logging.error(e.args)
    finally:
        # Always quit driver
        driver.quit()
