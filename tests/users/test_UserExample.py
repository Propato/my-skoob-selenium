# Standard imports
import sys, os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Imports specific to this test

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "baseClasses"))
from TestBase import TestBase


class TestUserExample(TestBase):
    # ========== Main Function ========== #
    def test_UserExample(self):
        self.directory = os.path.basename(os.path.dirname(os.path.abspath(__file__)))  # Set Directory

        self.Start(tab="Home")

        self.sleep(5)

        self.quit()

    # ========== Secondary Functions ========== #
    def nothing(self):
        pass
