from selenium import webdriver
from functions import login, composetweet, posttweet, scrapetweets, gowild

# Inputs to quit
quitChars = ["q", "Q", "quit", "Quit"]


# Main while loop that handles user inputs
# Makes calls to other functions based on user inputs
def main():
    try:
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
                login.login(browser)
                loggedin = True
            elif navigate == "composetweet":
                tweet = composetweet.composetweet()
                # Print the tweet for the person
                print(tweet)
            elif navigate == "scrape":
                scrapetweets.scrapeweets()
            # Ensure the user has logged in and a tweet has been composed first
            elif navigate == "posttweet":
                # Make sure the user is logged in
                if not loggedin:
                    print("You must log in first!")
                # Only if the user is logged in and has a tweet composed, post it
                else:
                    posttweet.posttweet(browser)
            elif navigate == "gowild":
                try:
                    # If the user enters a non int number it throws a value error exception
                    delay = int(input("Time delay in seconds between posts: "))
                    # Quickly ensure delay is an int
                    gowild.gowild(browser, delay)
                # Catch the exception and ask the user to enter an int next time
                except ValueError:
                    print("Please enter an integer value for the delay")
            # Prompt user to make another selection, also giving them a chance to end the loop
            navigate = input("What would you like to do? (login, composetweet, scrape, posttweet) ")

    finally:
        # Once the loop ends close the browser
        if browser is not None:
            browser.quit()


main()
