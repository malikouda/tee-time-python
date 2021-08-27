from credentials import get_credentials
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep


def submit_form(form_data, driver):
    for element_id, user_input in form_data:
        element = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        element.send_keys(user_input)

    element.submit()


def main():
    email, password = get_credentials(env_file="./secrets.env")

    try:
        driver = webdriver.Chrome()
        driver.get("https://magnolia-golf.book.teeitup.com/login")

        submit_form(
            form_data=[("txtUsername", email), ("txtPassword", password)], driver=driver
        )
    except Exception as e:
        print(e)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
