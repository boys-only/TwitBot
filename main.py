from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import common
# from selenium.webdriver.common.keys import Keys
import loginInfo
import markov
import re
from bs4 import BeautifulSoup
import requests

# Just global lists
# Affirmatives and negatives for prompts
affirmatives = ["yes", "Yes", "y", "Y", "1"]
negatives = ["No", "no", "N", "n", "0"]
# Inputs to quit
quitChars = ["q", "Q", "quit", "Quit"]
# List of people
people = ["kanye", "trump", "codyko", "noel miller", "spock music", "codynoelspock"]
# Maps of people and their respective twitter links and text files
profiledict = {
    "trump": "https://twitter.com/realDonaldTrump",
    "kanye": "https://twitter.com/kanyewest",
    "codyko": "https://twitter.com/codyko",
    "noel miller": "https://twitter.com/thenoelmiller",
    "spock music": "https://twitter.com/spockmusic"

}
textfiledict = {
    "trump": "trump.txt",
    "kanye": "kanye.txt",
    "codyko": "codynoelspock.txt",
    "noel miller": "codynoelspock.txt",
    "spock music": "codynoelspock.txt",
    "codynoelspock": "codynoelspock.txt"
}
tweetsizedict = {
    "s": 17,
    "m": 27,
    "l": 35
}


# Main while loop that handles user inputs
# Makes calls to other functions based on user inputs
def main():
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
    navigate = navigate.lower()
    # Loop runs until user opts to quit
    while navigate not in quitChars:
        if navigate == "login":
            login(browser)
            loggedin = True
        elif navigate == "composetweet":
            # Present the person with all the people options
            print("Your options are: ")
            for i in range(people.__len__()):
                print(people[i])
            # Ask them who they want to impersonate
            person = input("Who would you like to compose as? ")
            size = input("Tweet size? [s/m/l] ")
            # Compose a tweet using that person's text file
            tweet = composetweet(person.lower(),size)
            # Print the tweet for the person
            print(tweet)
        elif navigate == "scrape":
            scrapeweets()

        # Ensure the user has logged in and a tweet has been composed first
        elif navigate == "posttweet":
            # Make sure the user is logged in
            if not loggedin:
                print("You must log in first!")
            # Only if the user is logged in and has a tweet composed, post it
            else:
                posttweet(browser)
        # Prompt user to make another selection, also giving them a chance to end the loop
        navigate = input("What would you like to do? (login, composetweet, scrape, posttweet) ")
    # Once the loop ends close the browser
    browser.quit()


# Logs to bot into twitter on google chrome
def login(browser):
    try:
        # Send the bot to twitter
        browser.get("https://twitter.com")

        # Find login button and click
        # <input type="submit" class="EdgeButton EdgeButton--secondary EdgeButton--medium submit js-submit" value="Log in">
        # xpath: //*[@id=\"doc\"]/div/div[1]/div[1]/div[2]/div[2]/div/a[2]
        loginButton = browser.find_element_by_xpath("//*[@id=\"doc\"]/div/div[1]/div[1]/div[2]/div[2]/div/a[2]")
        loginButton.click()

        # Find username box and enter username
        # <input class="js-username-field email-input js-initial-focus" type="text" name="session[username_or_email]" autocomplete="on" value="" placeholder="Phone, email or username">
        # browser.find_element_by_css_selector("#page-container > div > div.signin-wrapper > form > fieldset > div:nth-child(2) > input")
        # Using this implementation waits until the item is present before trying to click it
        usernamebox = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#page-container > div > div.signin-wrapper > form > fieldset > div:nth-child(2) > input")))
        usernamebox.click()
        usernamebox.send_keys(loginInfo.username)

        # Find password box and enter password
        passwordbox = browser.find_element_by_xpath("//*[@id=\"page-container\"]/div/div[1]/form/fieldset/div[2]/input")
        passwordbox.click()
        passwordbox.send_keys(loginInfo.password)

        # Find and click log in
        # <button type="submit" class="submit EdgeButton EdgeButton--primary EdgeButtom--medium">Log in</button>
        loginButton = browser.find_element_by_xpath("//*[@id=\"page-container\"]/div/div[1]/form/div[2]/button")
        loginButton.click()

        print("Login successful!")
    # Catch this exception so you can still close the browser
    except common.exceptions.NoSuchElementException:
        print("Element not found")


# Composes a tweet based on the users preferred person and size
def composetweet(person, size):
    # Open the text file
    file = open(textfiledict.get(person), "r")
    # Construct a markov with the file
    mark = markov.Markov(file)
    # Create the map of the words
    mark.file_to_words()
    mark.triples()
    mark.database()
    # Generate a markov text
    text = mark.generate_markov_text(tweetsizedict.get(size))
    # print("First try \n", text + "\nTweet length: ", len(text))
    if len(text) < 280:
        print("Tweet composed!")
        text = filtertext(text)
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
                text = filtertext(text)
                return text.lower()


# Updates the text files for the given person by scraping tweets from there twitter
def scrapeweets():
    # Present options
    print("Your options are: ")
    for i in range(people.__len__()):
        print(people[i])
    # Get user input
    person = input("Who would you like to scrape? ")
    person = person.lower()
    # Ensure that selected person is in list
    if person in people:
        # Set the page to scrape and file to write to using the dictionaries
        page = requests.get(profiledict.get(person))
        file = open(textfiledict.get(person), "a+")

        # Soupfiy it
        souped = BeautifulSoup(page.text, 'html.parser')

        # Narrow search down to tweets
        # <p class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text" lang="en" data-aria-label-part="0">
        tweets = souped.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

        # For each tweet, remove all links and pictures, as well as periods and commas
        for i in tweets:
            result = filtertext(i.text)
            # print(result)
            file.write(result + "\n")
        print("Scrape successful!")
        file.close()
    else:
        print("Sorry, I can't scrape that person")



# Posts a composed tweet to the bots twitter account
def posttweet(browser):
    # Present options to user
    print("Your options are: ")
    for i in range(people.__len__()):
        print(people[i])
    # Get input from user
    person = input("Who would you like to tweet as? ")
    size = input("Tweet size? [s/m/l] ")
    tweet = composetweet(person.lower(), size)
    # Show the tweet to the user
    print(tweet)
    # Create a while loop that runs until the user either declines the tweet, or accepts a tweet
    # Rerolling does not break the loop so the user can reroll until they are satisfied or change their mind
    loop = True
    while loop:
        # Ask the user to confirm that the tweet should be sent
        # The idea is for each tweet to be proofread so that nothing terrible is said
        confirmpost = input("Confirm tweet? [y/n/reroll] ")
        # If the user approves of the tweet, continue with posting and break the loop
        if confirmpost in affirmatives:
            # Post the tweet
            # XPATH for draft box
            # //*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div
            draft = browser.find_element_by_xpath(
                "//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div")
            draft.send_keys(tweet)

            # Post button xpath
            # //*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/span/span
            postbutton = browser.find_element_by_xpath(
                "//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/span/span")
            postbutton.click()
            print("Tweet posted!")
            # End the loop
            loop = False
        # The user has elected to generate a new tweet
        elif confirmpost == "reroll":
            # Generate a new tweet using the same person
            tweet = composetweet(person.lower(), size)
            # Show newly generated tweet
            print(tweet)
        # The user has opted not to continue with the post. Breaks the loops and enters back into main loop
        else:
            loop = False



# Filters out periods, commas, links and other things
def filtertext(tweet):
    result = re.sub(r"http\S+", "", tweet)
    result = re.sub(r"pic\S+", "", result)
    result = re.sub(r"@\S+", "", result)
    result = result.replace('.', '')
    result = result.replace(',', '')
    # This one is for you cody/noel
    result = result.replace("tickets on sale", "")
    return result


main()
