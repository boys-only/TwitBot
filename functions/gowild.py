from functions import autopost, scrapetweets, login
import random
from listsanddicts import people


# This is a function to allow the bot to run continously until stopped
def gowild(browser):
    login.login(browser)
    # TODO create loop that runs indefinitely
    for i in range(29):
        # TODO Periodically tweet
        # TODO randomly pick someone from the list (NOT ALL)
        # Seed the random number generator
        random.seed()
        # Pick a random number in the range of the list
        randperson = people.people[random.randrange(0, people.people.__len__()-1)]
        # TODO randomly pick a size
        # Pick a random size
        sizes = ["s", "m", "l"]
        size = sizes[random.randrange(0, sizes.__len__()-1)]
        #autopost.autopost(browser, randperson, size)
        print(randperson)
        # TODO Periodically scrape everyone (once a day)