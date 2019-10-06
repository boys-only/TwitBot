from selenium import webdriver
from functions import login, composetweet, posttweet, scrapetweets, gowild
from gui import window
import sys
from PyQt5.QtWidgets import QApplication


# Inputs to quit
quitChars = ["q", "Q", "quit", "Quit"]


class main():
    def __init__(self):
        # Create the browser
        # Create chrome options to disable notifications
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        # Get the browser and open it
        self.browser = webdriver.Chrome(options=chrome_options)

        # Create the PyQt app and window
        self.app = QApplication(sys.argv)
        self.wind = window.MainWindow()

        # Connect the functions to their calls from main
        self.wind.loginbutton.clicked.connect(self.calllogin)

        self.wind.show()
        self.app.exec_()

    def calllogin(self):
        login.login(self.browser)



main().__init__()