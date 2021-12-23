import logging
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def handle_text_form(driver, **elements):
    for (element_id, data) in elements.items():
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        element.send_keys(data)

    element.submit()


def construct_url(base_url, **params):
    new_url = f"{base_url}/?"
    new_url += "&".join(
        [f"{param}={value}" for param, value in params.items() if value]
    )
    return new_url


def check_for_tee_times(driver):
    # wait until tee times are loaded or no tee times element is found
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//*[@data-testid='no-tee-times-found'] | //*[@data-testid='teetimes_book_now_button'] | //*[@data-testid='no-records-found']",
            )
        )
    )
    try:
        return (
            driver.find_element_by_xpath("//*[@data-testid='no-tee-times-found'] | //*[@data-testid='no-records-found']")
            == None
        )
    except NoSuchElementException as e:
        logging.warning("going ahead, assuming we found some tee times")
    return True


def book_earliest_date(driver):
    all_tee_times = WebDriverWait(driver, 1).until(
        EC.presence_of_all_elements_located(
            (
                By.CSS_SELECTOR,
                "[data-testid='teetimes_book_now_button']",
            )
        )
    )
    all_tee_times[0].click()

    # wait until player count button on next screen or locked tee time message appears
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//*[@data-testid='player-count'] | //*[@data-testid='main-alert-bar-message']",
            )
        )
    )


def continue_to_book(driver, golfers):
    try:
        driver.find_element_by_xpath("//*[@data-testid='player-count']")
    except NoSuchElementException as e:
        raise Exception("Couldn't find Player Count button, tee time is likely locked")

    num_golfers_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '[data-testid="player-count"] > button')
        )
    )
    if int(golfers) > len(num_golfers_buttons):
        num_golfers_buttons[-1].click()
    else:
        num_golfers_buttons[int(golfers) - 1].click()

    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[@data-testid='modal-rate-proceed-to-checkout-btn']")
        )
    )
    element.click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@data-testid='terms-and-conditions-checkbox']"))
    )
    element.click()

    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[@data-testid='email-opt-in-checkbox-checkout']")
        )
    )
    element.click()


def confirm_booking(driver, full_name, phone_number, notes, testing, cc_num, cc_month, cc_year, cc_cvv):
    # Card Number
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@placeholder='Card Number *']")
        )
    )

    if element.get_attribute('value').replace(" ", "") != cc_num:
        while element.get_attribute('value') != "":
            element.send_keys(Keys.BACKSPACE)
        element.send_keys(cc_num)

    # Card CVV
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "Payment.CC.CVVCode"))
    )

    if element.get_attribute('value') != cc_cvv:
        while element.get_attribute('value') != "":
            element.send_keys(Keys.BACKSPACE)
        element.send_keys(cc_cvv)
    
    # Card Month
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[@data-testid='credit-card-exp-month']")
        )
    )
    element.click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.ID, "menu-Payment.CC.ExpirationMonth")
        )
    )
    element = element.find_element_by_xpath(f".//li[@data-value='{cc_month}']")
    element.click()

    # Card year
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[@data-testid='credit-card-exp-year']")
        )
    )
    element.click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.ID, "menu-Payment.CC.ExpirationYear")
        )
    )
    element = element.find_element_by_xpath(f".//li[@data-value='{cc_year}']")
    element.click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "Payment.Name"))
    )

    if element.get_attribute("value") != full_name:
        while element.get_attribute("value") != "":
            element.send_keys(Keys.BACKSPACE)
        element.send_keys(full_name)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone-form-control"))
    )

    if element.get_attribute("value") != phone_number:
        while element.get_attribute("value") != "+":
            element.send_keys(Keys.BACKSPACE)
        element.send_keys(phone_number)

    if notes:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "Reservation.CustomerNotes"))
        )
        element.send_keys(notes)

    if not testing:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@data-testid='make-your-reservation-btn']")
            )
        )
        element.click()
