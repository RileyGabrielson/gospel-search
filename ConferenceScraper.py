import requests
from genconf import Conference
from genconf import Talk
from bs4 import BeautifulSoup
import pickle


def parseConferencesToFile(firstYear, lastYear):
    for i in range(firstYear, lastYear + 1):

        url = "https://www.churchofjesuschrist.org/study/general-conference/" + \
            str(i) + "/04?lang=eng"
        name = str(i) + " April Conference"
        parseSingleConference(url, name)

        url = "https://www.churchofjesuschrist.org/study/general-conference/" + \
            str(i) + "/10?lang=eng"
        name = str(i) + " October Conference"
        parseSingleConference(url, name)


def parseSingleConference(url, name):
    newConference = Conference(name)
    print("")
    print("--------Parsing " + name + "--------")
    newConference.parseByURL(url)
    with open("conferences/" + name + '.pickle', 'wb') as output:
        pickle.dump(newConference, output, pickle.HIGHEST_PROTOCOL)


#parseConferencesToFile(2003, 2020)
parseSingleConference("https://www.churchofjesuschrist.org/study/general-conference/" +
                      "2021" + "/04?lang=eng", "2021 April Conference")
