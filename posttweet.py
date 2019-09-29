import composetweet
from listsanddicts import yesandno


# Posts a composed tweet to the bots twitter account
def posttweet(browser):
    tweet = composetweet.composetweet()
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
        if confirmpost in yesandno.affirmatives:
            # Post the tweet
            # XPATH for draft box
            # //*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div
            draft = browser.find_element_by_xpath("//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div")
            draft.send_keys(tweet)

            # Post button xpath
            # //*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/span/span
            postbutton = browser.find_element_by_xpath("//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/span/span")
            postbutton.click()
            print("Tweet posted!")
            # End the loop
            loop = False
        # The user has elected to generate a new tweet
        elif confirmpost == "reroll":
            # Generate a new tweet using the same person
            tweet = composetweet.composetweet()
            # Show newly generated tweet
            print(tweet)
        # The user has opted not to continue with the post. Breaks the loops and enters back into main loop
        else:
            loop = False