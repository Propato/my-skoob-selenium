import json
import os
from selenium.webdriver.common.by import By

from tests.baseClasses.SeleniumMiddleware import SeleniumMiddleware


class TestBase(SeleniumMiddleware):
    def setup_method(self, method):
        super().setup_method(method)

        self.testName = method.__name__
        self.directory = os.path.basename(os.path.dirname(__file__))

        with open("data.json", "r") as file:
            self.data = json.load(file)

    def teardown_method(self, method):
        try:
            print(f"{self.directory}/{self.testName}: {self.driver.current_url}")
            with open("reports/report.txt", "a") as file:
                file.write(f"{self.directory}/{self.testName}\n")
        except:
            pass
        finally:
            super().teardown_method(method)

    def NavBar(self, tab):
        self.click((By.LINK_TEXT, tab))
        self.sleep()

    def Login(self, user, password):
        pass

    def Logout(self):
        pass

    def Start(
        self,
        url="",
        user="",
        password="",
        tab="",
    ):
        if url == "":
            url = self.data["url"]
        if user == "":
            user = self.data["user"]
        if password == "":
            password = self.data["password"]

        # Try-Except: Try again if something went wrong
        try:
            self.open_url(url)
        except:
            self.refresh()
            self.open_url(url)
        self.sleep(1)

        # Try-Except: Try again if something went wrong
        try:
            self.Login(user, password)
        except:
            self.refresh()
            self.Login(user, password)

        try:
            self.NavBar(tab)
        except:
            self.refresh()
            self.NavBar(tab)
