from bs4 import BeautifulSoup
import requests
import re
import datetime

textfiledict = {
    "trump": "./textfiles/trump.txt",
    "kanye": "./textfiles/kanye.txt",
    "dril": "./textfiles/dril.txt",
    "wendy": "./textfiles/wendy.txt",
    "harvard": "./textfiles/harvard.txt",
    "beans": "./textfiles/beans.txt",
    "all": "/home/pi/Documents/TwitBot/textfiles/all.txt"
}

profiledict = {
    "trump": "https://twitter.com/realDonaldTrump",
    "kanye": "https://twitter.com/kanyewest",
    "dril": "https://twitter.com/dril",
    "wendy": "https://twitter.com/Wendys",
    "harvard": "https://twitter.com/heelyfanaccount",
    "beans": "https://twitter.com/goodbeanalt"
}
people = ["kanye", "trump", "dril", "wendy", "harvard", "beans", "all"]

def filtertext(tweet):
    result = re.sub(r"http\S+", "", tweet)
    result = re.sub(r"pic\S+", "", result)
    result = re.sub(r"@\S+", "", result)
    result = result.replace('.', '')
    result = result.replace(',', '')
    # This one is for you cody/noel
    result = result.replace("tickets on sale", "")
    result = result.replace("tmg", "")
    result = result.replace("LOVE ISLAND", "")
    result = result.replace("tickets on sale", "")

    return result

def checkforduplicates(person, text):
    # Check the person's file for the current tweet
    with open('/home/pi/Documents/TwitBot/textfiles/all.txt') as file:
        filelines = file.readlines()
    for line in filelines:
        if text in line:
#            print("Duplicate Found")
#            print(text)
            return True
    return False

# Go through the list of people
# Open the text file for everyone
allfile = open(textfiledict.get("all"), "a+")
for i in range(people.__len__() - 1):
    person = people[i]
    print(person)
    # Set the page to scrape and file to write to using the dictionaries
    page = requests.get(profiledict.get(person))
    
    

    # Soupfiy it
    souped = BeautifulSoup(page.text, 'html.parser')

    # Narrow search down to tweets
    # <p class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text" lang="en" data-aria-label-part="0">
    tweets = souped.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

    # For each tweet, remove all links and pictures, as well as periods and commas
    for j in tweets:
        result = filtertext(j.text)
        if not checkforduplicates(person, result):
            
            allfile.write(result + "\n")

    print("Scrape successful!")
    now = datetime.datetime.now()
    print(str(now))
allfile.close()
