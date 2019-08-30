from selenium import webdriver
from selenium import common
from selenium.webdriver.common.keys import Keys
import loginInfo
import time


def main():
    # Affirmatives and negatives for prompts
    affirmatives = ["yes", "Yes", "y", "Y"]
    negatives = ["No", "no", "N", "n"]
    
    # Create chrome options to disable notifications
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    # Get the browser and open it
    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()

    try:
        # Send the bot to twitter
        browser.get("https://twitter.com")

        # Login to twitter
        login(browser)

        # Prompt user and ask if they want to compose a tweet

        proceed = input("Create tweet? [y/n]: ")

        if proceed in affirmatives:
            composeTweet(browser)
        else:
            pass

    finally:
        quitChars = ["q", "Q"]
        quiter = input("Enter Q to close browser")
        while quiter not in quitChars:
            if quiter == "q" or quiter == "Q":
                browser.quit()
            else:
                quiter = input("Enter Q to close browser")


def login(browser):
    try:
        # Login button
        # <input type="submit" class="EdgeButton EdgeButton--secondary EdgeButton--medium submit js-submit" value="Log in">
        # xpath: //*[@id=\"doc\"]/div/div[1]/div[1]/div[2]/div[2]/div/a[2]
        loginButton = browser.find_element_by_xpath("//*[@id=\"doc\"]/div/div[1]/div[1]/div[2]/div[2]/div/a[2]")
        loginButton.click()

        # Wait a minute
        time.sleep(5)

        # Enter username
        # <input class="js-username-field email-input js-initial-focus" type="text" name="session[username_or_email]" autocomplete="on" value="" placeholder="Phone, email or username">
        usernamebox = browser.find_element_by_css_selector("#page-container > div > div.signin-wrapper > form > fieldset > div:nth-child(2) > input")
        usernamebox.click()
        usernamebox.send_keys(loginInfo.username)

        # Enter password
        passwordbox = browser.find_element_by_xpath("//*[@id=\"page-container\"]/div/div[1]/form/fieldset/div[2]/input")
        passwordbox.click()
        passwordbox.send_keys(loginInfo.password)

        # Click log in
        # <button type="submit" class="submit EdgeButton EdgeButton--primary EdgeButtom--medium">Log in</button>
        loginButton = browser.find_element_by_xpath("//*[@id=\"page-container\"]/div/div[1]/form/div[2]/button")
        loginButton.click()

    # Catch this exception so you can still close the browser
    except common.exceptions.NoSuchElementException:
        print("Element not found")


def composeTweet(browser):
    pass

main()