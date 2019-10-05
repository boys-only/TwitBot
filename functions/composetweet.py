from listsanddicts import textfiledict, sizedict, people
from functions import filtertext, getperson, markov


# Composes a tweet based on the users preferred person and size
def composetweet():
    # Prompt user for desired person
    person = getperson.getperson()
    # Make sure the user isn't trying to tweet as everyone
    # I can do this in the future
    # if person == "all":
    #     return "Sorry I can't tweet from everyone. Maybe in the future."
    if person in people.people:
        # Prompt user for desired size of tweet
        size = input("Tweet size? [s/m/l] ")
        while size not in ["s", "m", "l"]:
            print("Invalid size")
            size = input("Tweet size? [s/m/l] ")
        # Compose a tweet using that person's text file
        # Open the text file
        file = open(textfiledict.textfiledict.get(person), "r")
        # Construct a markov with the file
        mark = markov.Markov(file)
        # Create the map of the words
        mark.file_to_words()
        mark.triples()
        mark.database()
        # Generate a markov text
        text = mark.generate_markov_text(sizedict.tweetsizedict.get(size))
        # print("First try \n", text + "\nTweet length: ", len(text))
        if len(text) < 280:
            print("Tweet composed!")
            text = filtertext.filtertext(text)
            return text.lower()
        else:
            # While the text is longer than 280 chars, keep generating new texts
            while len(text) > 280:
                # Generate a new text
                text = mark.generate_markov_text(size)
                # print(text + "\nTweet length: ", len(text))
                # If it is less than 280 chars, return it
                if len(text) < 280:
                    # print(text + "\nTweet length: ", len(text))
                    file.close()
                    print("Tweet composed!")
                    text = filtertext.filtertext(text)
                    return text.lower()
    else:
        print("Invalid person")
