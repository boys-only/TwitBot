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
    affirmatives = ["yes", "Yes", "y", "Y", "1"]
    negatives = ["No", "no", "N", "n", "0"]
    quitChars = ["q", "Q", "quit", "Quit"]
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
            loggedin = True
        elif navigate == "composetweet":
            tweet = composetweet()
            print(tweet)
        elif navigate == "scrape":
            scrapetrumptweets()
        # Ensure the user has logged in and a tweet has been composed first
        elif navigate == "posttweet":
            # Make sure the user is logged in
            if not loggedin:
                print("You must log in first!")
            # Only if the user is logged in and has a tweet composed, post it
            else:
                tweet = composetweet()
                print(tweet)
                loop = True
                while loop:
                    confirmpost = input("Confirm tweet? [y/n] ")
                    if confirmpost in affirmatives:
                        posttweet(tweet, browser)
                        loop = False
                    elif confirmpost == "reroll":
                        tweet = composetweet()
                        print(tweet)
                    else:
                        loop = False
        navigate = input("What would you like to do? (login, composetweet, scrape, posttweet) ")
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
        print("Tweet composed!")
        text = text.replace('.', '')
        text = text.replace(',', '')
        return text.lower()
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
                print("Tweet composed!")
                text = text.replace('.', '')
                text = text.replace(',', '')
                return text.lower()


def scrapetrumptweets():
    # Request DT's twitter page
    page = requests.get("https://twitter.com/realDonaldTrump")

    # Soupfiy it
    souped = BeautifulSoup(page.text, 'html.parser')

    # Narrow search down to tweets
    # <p class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text" lang="en" data-aria-label-part="0">
    tweets = souped.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    file = open("trump.txt", "a+")
    for i in tweets:
        result = re.sub(r"http\S+", "", i.text)
        result = re.sub(r"pic\S+", "", result)
        result = re.sub(".", "", result)
        result = re.sub(",", "", result)
        print(result)
        file.write(result + "\n")
    file.close()


def posttweet(tweet, browser):
    # XPATH for draft box
    # //*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div
    draft = browser.find_element_by_xpath("//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div")
    draft.send_keys(tweet)

    # Post button xpath
    # //*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/span/span
    postbutton = browser.find_element_by_xpath("//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/span/span")
    postbutton.click()
    print("Tweet posted!")

main()