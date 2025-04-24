# Standard imports
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Imports specific to this test

from tests.baseClasses.TestBase import TestBase


class TestUserExemplo(TestBase):
    # ========== Main Function ========== #
    def test_UserExemplo(self):
        self.directory = os.path.basename(os.path.dirname(os.path.abspath(__file__)))  # Set Directory

        self.Start(tab="Home")

        self.sleep(5)

        self.quit()

    # ========== Secondary Functions ========== #
    def nothing(self):
        pass
