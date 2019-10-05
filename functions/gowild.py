import time

from functions import autopost, scrapetweets, login
import random
from listsanddicts import people


# This is a function to allow the bot to run continuously until stopped
# * * *
# Currently to stop you need to induce a keyboard interrupt
# Either by using ^C (Control C), or by attempting to stop the program in the IDE
# * * *
def gowild(browser, delay):
    login.login(browser)
    try:
        while True:
            # TODO create loop that runs indefinitely
            # TODO Periodically tweet
            # TODO randomly pick someone from the list (NOT ALL)
            # Seed the random number generator
            random.seed()

            # Pick a random number in the range of the list, and retrieve that person from the list
            randperson = people.people[random.randrange(0, people.people.__len__() - 1)]
            # TODO randomly pick a size
            # Pick a random size
            sizes = ["s", "m", "l"]
            # Actually get that size from the dictionary
            size = sizes[random.randrange(0, sizes.__len__() - 1)]
            # Post it
            autopost.autopost(browser, randperson, size)
            # Time delay in seconds between tweets
            print(randperson)
            time.sleep(delay)
            # TODO Periodically scrape everyone (once a day)
    except KeyboardInterrupt:
        pass
