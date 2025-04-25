# Standard imports
import os

# Imports the TestBase class from baseClasses
from baseClasses.BaseTest import BaseTest

# Imports specific to this test


class TestReviewExample(BaseTest):
    # ========== Main Function ========== #
    def test_ReviewExample(self):
        self.directory = os.path.basename(os.path.dirname(os.path.abspath(__file__)))  # Set Directory

        self.Start(tab="Reviews")

        self.sleep(5)

        self.quit()

    # ========== Secondary Functions ========== #
    def nothing(self):
        pass
