from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import loginInfo


def main():
    # Create chrome options to disable notifications
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    # Get the browser and open it
    browser = webdriver.Chrome(options=chrome_options)

    # TODO: Create a list of words that can be used to form a tweet
    # TODO: Create a method of composing tweets

    browser.get("https://google.com")


main()