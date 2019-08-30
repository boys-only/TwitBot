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

    try:

        # Send the bot to twitter
        browser.get("https://twitter.com")

        # TODO: Create a list of words that can be used to form a tweet
        # TODO: Create a method of composing tweets
        # Limit tweet to 240 chars

    finally:
        quitChars = ["q", "Q"]
        quit = input("Enter Q to close browser")
        while quit not in quitChars:
            if quit == "q" or quit == "Q":
                browser.quit()
            else:
                quit = input("Enter Q to close browser")




main()