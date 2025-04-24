import time
import json
import sys, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class SeleniumMiddleware:
    def setup_method(self, method):

        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-dev-shm-usage")

        if not os.getenv("SELENIUM_LOCAL"):
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")

        self.driver = webdriver.Remote(command_executor="http://selenium_hub:4444/wd/hub", options=options)

        self.testName = method.__name__
        self.directory = os.path.basename(os.path.dirname(__file__))

    def teardown_method(self, method):
        try:
            self.driver.save_screenshot(f"./prints/{self.directory}/{self.testName}.png")
            self.driver.quit()
        except:
            try:
                self.driver.quit()  # Verify if the driver is still running
                print(f"Driver quit: {self.directory}/{self.testName}")
            except:
                print(f"Driver already quit: {self.directory}/{self.testName}")

    #################################################################################
    ################################ USEFUL FUNCTIONS ###############################
    #################################################################################

    def sleep(self, time=1):
        time.sleep(time)

    def script(self, script):
        self.driver.execute_script(script)

    def open_url(self, url):
        self.driver.get(url)
        time.sleep(1)

    def refresh(self):
        self.driver.refresh()
        time.sleep(1)

    def quit(self):
        self.driver.quit()

    #################################################################################
    ############################# INTERACTION FUNCTIONS #############################
    #################################################################################

    def click(self, element, time=10):
        WebDriverWait(self.driver, time).until(expected_conditions.element_to_be_clickable(element)).click()

    def clear(self, element, time=10):
        WebDriverWait(self.driver, time).until(expected_conditions.element_to_be_clickable(element)).clear()

    def press_key(self, element, key, time=10):
        WebDriverWait(self.driver, time).until(expected_conditions.element_to_be_clickable(element)).send_keys(key)

    def send_text(self, element, text, time=10):
        WebDriverWait(self.driver, time).until(expected_conditions.element_to_be_clickable(element)).clear()
        WebDriverWait(self.driver, time).until(expected_conditions.element_to_be_clickable(element)).send_keys(text)

    def send_date(self, element, date, time=10, limit=5):
        formatted_date = f"{date[:2]}/{date[2:4]}/{date[4:]}"

        while limit > 0:
            WebDriverWait(self.driver, time).until(expected_conditions.element_to_be_clickable(element)).clear()
            WebDriverWait(self.driver, time).until(expected_conditions.element_to_be_clickable(element)).send_keys(date)
            time.sleep(1)
            if (
                WebDriverWait(self.driver, time)
                .until(expected_conditions.element_to_be_clickable(element))
                .get_attribute("value")
                == formatted_date
            ):  # Verify if the date is correct
                break
            limit -= 1

        if limit <= 0:
            print(
                "Value: ",
                WebDriverWait(self.driver, time)
                .until(expected_conditions.element_to_be_clickable(element))
                .get_attribute("value"),
            )
            raise Exception("Set Date: Limit exceeded")

    def accept_alert(self, time=10, delay=1):
        self.delay(delay)
        WebDriverWait(self.driver, time).until(lambda driver: driver.switch_to.alert).accept()
        self.delay(delay)

    #################################################################################
    ############################## GET VALUES FUNCTIONS #############################
    #################################################################################

    def get_text(self, element, time=10):
        return WebDriverWait(self.driver, time).until(expected_conditions.element_to_be_clickable(element)).text

    def get_attribute(self, element, attribute, time=10):
        return (
            WebDriverWait(self.driver, time)
            .until(expected_conditions.element_to_be_clickable(element))
            .get_attribute(attribute)
        )

    #################################################################################
    ################################ SELECT FUNCTIONS ###############################
    #################################################################################

    def select_option(self, element, text, time=10):
        Select(
            WebDriverWait(self.driver, time).until(expected_conditions.element_to_be_clickable(element))
        ).select_by_visible_text(text)

    def get_select_num_options(self, element, time=10):
        return len(
            WebDriverWait(self.driver, time)
            .until(expected_conditions.element_to_be_clickable(element))
            .find_elements(By.TAG_NAME, "option")
        )

    def get_selected_text(self, element, time=10):
        return Select(
            WebDriverWait(self.driver, time).until(expected_conditions.element_to_be_clickable(element))
        ).first_selected_option.text

    #################################################################################
    ################################ AWAIT FUNCTIONS ################################
    #################################################################################

    def await_text(self, element, text, time=10):
        WebDriverWait(self.driver, time).until(expected_conditions.text_to_be_present_in_element(element, text))

    def await_attribute_not_empty(self, element, attribute, time=10):
        WebDriverWait(self.driver, time).until(
            lambda driver: driver.find_element(element[0], element[1]).get_attribute(attribute) != ""
        )

    def await_clickable(self, element, time=10):
        WebDriverWait(self.driver, time).until(expected_conditions.element_to_be_clickable(element))

    def await_n_window(self, n=1, time=30):
        WebDriverWait(self.driver, time).until(lambda driver: len(driver.window_handles) > n)

    def await_load(self, xpath, time=10):
        time.sleep(1)
        WebDriverWait(self.driver, time).until(
            lambda driver: False if driver.find_elements(By.XPATH, xpath) else True
        )  # Wait for loading component to close
        time.sleep(1)

    #################################################################################
    ################################ SWITCH FUNCTIONS ###############################
    #################################################################################

    def switch_to_window(self, window=0):
        self.driver.switch_to.window(self.driver.window_handles[window])

    def switch_to_frame(self, frame=1, time=30):
        WebDriverWait(self.driver, time).until(lambda driver: driver.switch_to.frame(frame) or True)

    def switch_to_default(self, time=30):
        WebDriverWait(self.driver, time).until(lambda driver: driver.switch_to.default_content() or True)
