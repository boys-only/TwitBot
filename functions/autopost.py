from selenium.webdriver.support.wait import WebDriverWait

from functions import autocompose
from listsanddicts import yesandno
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# This is meant to be used in the go wild function, it is similar to the post tweet function but accepts parameters and
# Does not confirm before posting. Also does not offer rerolls


# Posts a composed tweet to the bots twitter account
def autopost(browser, person, size):
    tweet = autocompose.autocompose(person, size)
    # Show the tweet to the user
    print(tweet)

    # Post the tweet
    # XPATH for draft box
    # //*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div
    draft = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div")))
    # draft = browser.find_element_by_xpath("//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div")
    draft.send_keys(tweet)

    # Post button xpath
    # //*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/span/span
    postbutton = browser.find_element_by_xpath("//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/span/span")
    postbutton.click()
    print("Tweet posted!")
