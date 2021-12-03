from genconf import Conference
from genconf import Talk
import pickle
from collections import Counter
import os
import random
from matplotlib import pyplot as plt
from collections import OrderedDict


def loadConference(fileName):
    conference = None
    with open(fileName, 'rb') as file:
        conference = pickle.load(file)
    return conference


def loadAllConferences():
    conferences = dict()
    for root, dirs, files in os.walk("./conferences", topdown=False):
        for file in files:
            if file.endswith(".pickle"):
                newConference = loadConference(os.path.join(root, file))
                conferences[newConference.name] = newConference

    return OrderedDict(sorted(conferences.items()))


def getAllTalks(conferences):
    talks = set()
    for c in conferences:
        for talk in conferences[c].talks:
            talks.add(talk)
    return talks


def mostCommonWords(talks, stop_words):
    counts = Counter()
    i = 1

    for talk in talks:
        if(i % 75 != 0):
            print('.', end='')
        else:
            print('.')
        i += 1
        paragraphs = talk.paragraphs
        for p in paragraphs:
            pList = p.split()
            counts += Counter(x.lower()
                              for x in pList if x.lower() not in stop_words)

    print("Most Common Words")
    print(counts.most_common(25))


def loadWords(fileName):
    stop_words = None
    with open(fileName, 'r') as file:
        words = file.read()
        stop_words = set(words.split())
    return stop_words


def printTalks(conference):
    talks = conference.talks
    for talk in talks:
        print(str(talk))


def wordOccurences(word, conferences):
    word = word.lower()
    occurences = []
    for conf in conferences:
        wordCount = 0
        talks = conferences[conf].talks
        for talk in talks:
            paragraphs = talk.paragraphs
            for paragraph in paragraphs:
                low_paragraph = paragraph.lower()
                wordCount += low_paragraph.count(word)
        occurences.append((conf, wordCount))
    return occurences


def talksBySpeaker(speaker, conferences):
    authorTalks = []
    for conf in conferences:
        for talk in conferences[conf].talks:
            if speaker.lower() in talk.author.lower():
                authorTalks.append(talk)
    return authorTalks


def plotOccurences(occurencesList, labels):
    x = []
    yList = []
    y = []
    updateX = True
    axis = plt.subplot(111)
    for occurences in occurencesList:
        for i in range(int(len(occurences))):
            if(updateX):
                x.append(occurences[i][0])
            y.append(occurences[i][1])
        updateX = False
        yList.append(y)
        y = []

    for i in range(0, len(yList)):
        axis.plot(x, yList[i], label=labels[i])
    axis.set_xticklabels([])
    axis.legend()
    plt.title("Occurences: " + str(labels))
    plt.ylabel("Occurences")
    plt.xlabel("1971-2020")
    plt.show()


def printParenValues(conferences):
    values = dict()
    for conf in conferences:
        for talk in conferences[conf].talks:
            for par in talk.paragraphs:
                paren_index = -1
                for i in range(0, len(par)):
                    if par[i] == '(':
                        paren_index = i
                    elif par[i] == ')':
                        value = par[paren_index+1:i]
                        value = value.replace('.', '')
                        if value.isdigit():
                            break
                        if value[0:4] == "see ":
                            value = value[4:]
                        if value in values:
                            values[value] += 1
                        else:
                            values[value] = 1
    for v in values:
        if values[v] > 30:
            print(v + " " + str(values[v]))


def occurence_loop():
    conferences = loadAllConferences()

    user_input = ""
    while user_input != 'q':
        print("Word Occurences")
        print("Type q to quit")
        user_input = input("Enter a word to search: ")
        if user_input == 'q':
            break
        print("---Searching all conferences for " + user_input + "---")
        occurences = wordOccurences(user_input, conferences)
        plotOccurences(occurences)


def searchByTitle(terms, conferences):
    search_Talks = []
    search_Conf = []

    for conf in conferences:
        for talk in conferences[conf].talks:
            result = [elem for elem in terms if(
                elem.lower() in talk.title.lower())]
            if len(result) == len(terms):
                search_Talks.append(talk)
                search_Conf.append(conf)

    return search_Talks, search_Conf


def randomTalk(conferences):
    conf = random.choice(list(conferences.values()))
    return random.choice(conf.talks), conf


def searchByContent(terms, conferences):
    search_Talks = []
    search_Conf = []
    paragraphs = []

    for conf in conferences:
        for talk in conferences[conf].talks:
            for p in talk.paragraphs:
                result = [elem for elem in terms if(elem in p.lower())]
                if len(result) == len(terms):
                    search_Talks.append(talk)
                    search_Conf.append(conf)
                    paragraphs.append(p)

    return paragraphs, search_Talks, search_Conf


def searchByContentExact(phrase, conferences):
    search_Talks = []
    search_Conf = []
    paragraphs = []
    phrase = phrase.lower()

    for conf in conferences:
        for talk in conferences[conf].talks:
            for p in talk.paragraphs:
                if phrase in p.lower():
                    search_Talks.append(talk)
                    search_Conf.append(conf)
                    paragraphs.append(p)

    return paragraphs, search_Talks, search_Conf
