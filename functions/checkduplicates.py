from listsanddicts import textfiledict


# Checks text files for duplications from scraped tweets
# Returns true if a tweet is already in the file
def checkforduplicates(person, text):
    # Check the person's file for the current tweet
    with open(textfiledict.textfiledict.get(person)) as file:
        filelines = file.readlines()
    for line in filelines:
        if text in line:
            print("Duplicate Found")
            return True
    return False
