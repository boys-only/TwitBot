from bs4 import BeautifulSoup
import requests
from listsanddicts import textfiledict, profiledict, people
from functions import checkduplicates, filtertext, getperson


# Updates the text files for the given person by scraping tweets from there twitter
def scrapeweets():
    # Get person
    person = getperson.getperson()
    # Ensure that selected person is in list and is not everyone on that list
    if (person in people.people) and person != "all":
        # Set the page to scrape and file to write to using the dictionaries
        page = requests.get(profiledict.profiledict.get(person))
        file = open(textfiledict.textfiledict.get(person), "a+")

        # Soupfiy it
        souped = BeautifulSoup(page.text, 'html.parser')

        # Narrow search down to tweets
        # <p class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text" lang="en" data-aria-label-part="0">
        tweets = souped.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

        # For each tweet, remove all links and pictures, as well as periods and commas
        for i in tweets:
            # Filter the tweet
            result = filtertext.filtertext(i.text)
            # If the tweet isn't not already in the file write it
            if not checkduplicates.checkforduplicates(person, result):
                file.write(result + "\n")

        print("Scrape successful!")
        file.close()
    # Scrape every person
    elif person == "all":
        # Go through the list of people
        for i in range(people.people.__len__() - 1):
            person = people.people[i]
            print(person)
            # Set the page to scrape and file to write to using the dictionaries
            page = requests.get(profiledict.profiledict.get(person))
            file = open(textfiledict.textfiledict.get(person), "a+")

            # Soupfiy it
            souped = BeautifulSoup(page.text, 'html.parser')

            # Narrow search down to tweets
            # <p class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text" lang="en" data-aria-label-part="0">
            tweets = souped.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

            # For each tweet, remove all links and pictures, as well as periods and commas
            for j in tweets:
                result = filtertext.filtertext(j.text)
                if not checkduplicates.checkforduplicates(person, result):
                    file.write(result + "\n")

            print("Scrape successful!")
            file.close()
    else:
        print("Sorry, I can't scrape that person")