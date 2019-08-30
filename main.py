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

        # Login to twitter
        login(browser)
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


def login(browser):
    # Login button
    # <input type="submit" class="EdgeButton EdgeButton--secondary EdgeButton--medium submit js-submit" value="Log in">
    # xpath: //*[@id=\"doc\"]/div/div[1]/div[1]/div[2]/div[2]/div/a[2]
    loginButton = browser.find_element_by_xpath("//*[@id=\"doc\"]/div/div[1]/div[1]/div[2]/div[2]/div/a[2]")
    loginButton.click()

    # Enter username
    usernamebox = browser.find_element_by_xpath("//*[@id=\"page-container\"]/div/div[1]/form/fieldset/div[1]/input")
    usernamebox.click()
    usernamebox.send_keys(loginInfo.username)

    # Enter password
    passwordbox = browser.find_element_by_xpath("//*[@id=\"page-container\"]/div/div[1]/form/fieldset/div[2]/input")
    passwordbox.click()
    passwordbox.send_keys(loginInfo.password)



main()