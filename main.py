from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import common
from selenium.webdriver.common.keys import Keys
import loginInfo
import time
import markov
import re
from bs4 import BeautifulSoup
import requests


def main():
    # Affirmatives and negatives for prompts
    affirmatives = ["yes", "Yes", "y", "Y"]
    negatives = ["No", "no", "N", "n"]
    quitChars = ["q", "Q"]
    tweet = None
    loggedin = False
    # Create chrome options to disable notifications
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    # Get the browser and open it
    browser = webdriver.Chrome(options=chrome_options)
    # If it can't for some reason find the window, use this
    # window = browser.current_window_handle
    # browser.switch_to.window(window)

    # The user can use the console to to various things
    navigate = input("What would you like to do? (login, composetweet, scrape, posttweet) ")
    while navigate not in quitChars:
        if navigate == "login":
            login(browser)
            main.loggedin = True
        elif navigate == "composetweet":
            tweet = composetweet()
            print(tweet)
        elif navigate == "scrape":
            scrapetrumptweets()
        # Ensure the user has logged in and a tweet has been composed first
        elif navigate == "posttweet" and tweet is not None :#and loggedin:
            posttweet(tweet, browser)
        navigate = input("What would you like to do? (login, composetweet, scrape) ")
    browser.quit()


def login(browser):
    try:
        # Send the bot to twitter
        browser.get("https://twitter.com")

        # Login button
        # <input type="submit" class="EdgeButton EdgeButton--secondary EdgeButton--medium submit js-submit" value="Log in">
        # xpath: //*[@id=\"doc\"]/div/div[1]/div[1]/div[2]/div[2]/div/a[2]
        loginButton = browser.find_element_by_xpath("//*[@id=\"doc\"]/div/div[1]/div[1]/div[2]/div[2]/div/a[2]")
        loginButton.click()

        # Enter username
        # <input class="js-username-field email-input js-initial-focus" type="text" name="session[username_or_email]" autocomplete="on" value="" placeholder="Phone, email or username">
        # browser.find_element_by_css_selector("#page-container > div > div.signin-wrapper > form > fieldset > div:nth-child(2) > input")
        # Using this implementation waits until the item is present before trying to click it
        usernamebox = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#page-container > div > div.signin-wrapper > form > fieldset > div:nth-child(2) > input")))
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

        print("Login successful!")
    # Catch this exception so you can still close the browser
    except common.exceptions.NoSuchElementException:
        print("Element not found")


def composetweet():
    # Open the text file
    file = open("trump.txt", "r")
    # Construct a markov with the file
    mark = markov.Markov(file)
    # Create the map of the words
    mark.file_to_words()
    mark.triples()
    mark.database()
    # Generate a markov text
    text = mark.generate_markov_text()
    # print("First try \n", text + "\nTweet length: ", len(text))
    if len(text) < 280:
        return text
    else:
        # While the text is longer than 280 chars, keep generating new texts
        while len(text) > 280:
            # Generate a new text
            text = mark.generate_markov_text()
            # print(text + "\nTweet length: ", len(text))
            # If it is less than 280 chars, return it
            if len(text) < 280:
                # print(text + "\nTweet length: ", len(text))
                file.close()
                return text


def scrapetrumptweets():
    # Request DT's twitter page
    page = requests.get("https://twitter.com/realDonaldTrump")

    # Soupfiy it
    souped = BeautifulSoup(page.text, 'html.parser')

    # Narrow search down to tweets
    # <p class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text" lang="en" data-aria-label-part="0">
    tweets = souped.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    file = open("trump.txt", "w+")
    for i in tweets:
        result = re.sub(r"http\S+", "", i.text)
        result = re.sub(r"pic\S+", "", result)
        print(result)
        file.write(result + "\n")


def posttweet(tweet, browser):
    print(tweet)

main()