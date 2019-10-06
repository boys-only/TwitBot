from selenium import webdriver
from functions import login, composetweet, posttweet, scrapetweets, gowild
from gui import window
import sys
from PyQt5.QtWidgets import QApplication


# Inputs to quit
quitChars = ["q", "Q", "quit", "Quit"]


# Main is now a class, as it should have been
class TwitBot:
    # The constructor for main now creates the browser, and also creates the display window
    # Along with this, it also connects the functions that can be called to the buttons on the window
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
        # It is easiest to just place each function in a wrapper function, and assign the wrapper to a button
        # It makes it easier to pass parameters and such
        self.wind.loginbutton.clicked.connect(self.calllogin)
        self.wind.scrapebutton.clicked.connect(self.callscrapetweets)

        # Make sure to show the window
        self.wind.show()
        # Actually executes the gui
        sys.exit(self.app.exec_())

    def calllogin(self):
        login.login(self.browser)

    @staticmethod
    def callcomposetweet():
        composetweet.composetweet()

    def callposttweet(self):
        posttweet.posttweet(self.browser)

    @staticmethod
    def callscrapetweets():
        scrapetweets.scrapeweets()

    # Right now the delay is static at 2 mins
    # Need a way to pass the delay from the window in
    def callwild(self):
        gowild.gowild(self.browser, 120)


def main():
    bot = TwitBot()
    try:
        bot.__init__()
    finally:
        bot.browser.close()

if __name__ == "__main__":
    main()
