from listsanddicts import people


# Gets person from user input
def getperson():
    # TODO Function that gets person from user input
    # Present options
    print("Your options are: ")
    for i in range(people.people.__len__()):
        print(people.people[i])
    # Get user input
    person = input("Which person would you like to select? ")
    person = person.lower()
    return person
