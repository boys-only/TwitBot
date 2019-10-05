import re


# Filters out periods, commas, links and other things
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
