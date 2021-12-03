from matplotlib import use
from genconf import Conference
from genconf import Talk
from os import system, name
import ConferenceAnalyzer as ca
import ScriptureAnalyzer as sa
import textwrap
from journal import load_all_journals, save_journal, Journal, Note


def mainLoop():
    conferences = ca.loadAllConferences()
    works = sa.loadAllWorks()
    clearScreen()
    print("Welcome to the Gospel Search Program")
    print("")
    printCommands()

    user_input = ""
    try:
        while user_input != 'q':
            user_input = input("Enter a command: ")
            print("")
            user_quit = parseUserInput(user_input, conferences, works)
            if user_quit:
                break
    except KeyboardInterrupt:
        print("Program Terminated")
        print("Goodbye")


def clearScreen():
    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')


def printCommands():
    print()
    print("\t" + "--------Commands--------")
    print("")
    print("Standard Works and General Conference:")
    print()
    print("\t" + "c: search by content")
    print("\t" + "x: search by content exactly")
    print("\t" + "b: browse")
    print()
    print("General Conference Only:")
    print()
    print("\t" + "t: search by title")
    print("\t" + "s: search by speaker")
    print("\t" + "d: search by date")
    print("\t" + "o: word occurences")
    print("\t" + "r: random talk")
    print("\t" + "q: quit")
    print()
    print("Study:")
    print()
    print("\t" + "j: Journals")
    print("")


def parseUserInput(input, conferences, works):
    clearScreen()
    input = input.lower()
    if input == 'q' or input == 'quit':
        return True
    elif input == 'c':
        searchContent(conferences, works)
        return False
    elif input == 'x':
        searchContent(conferences, works, exact=True)
    elif input == 'b':
        browse(conferences, works)
        return False
    elif input == 't':
        searchTitle(conferences)
        return False
    elif input == 's':
        searchSpeaker(conferences)
        return False
    elif input == 'd':
        searchDate(conferences)
        return False
    elif input == 'o':
        wordOccurences(conferences)
        return False
    elif input == 'r' or input == 'random':
        randomTalk(conferences)
    elif input == 'j':
        viewAllJournals()
    elif input == 'clear':
        return False
    else:
        printCommands()
        return False


def searchDate(conferences):
    print("-Search By Date-")
    search_term = input("Enter a conference (ex: october 1989): ")
    terms = breakUpSearch(search_term)
    print("")
    index = 0
    search_Conf = []
    search_Talks = []

    for conf in conferences:
        result = [elem for elem in terms if(
            elem in conferences[conf].name.lower())]
        if len(result) == len(terms):
            print(conf)
            print("")
            for talk in conferences[conf].talks:
                search_Conf.append(conf)
                search_Talks.append(talk)
                print("<" + str(index) + ">: " + str(talk.title))
                print("\t" + str(talk.author))
                print("\t" + str(conf))
                print("")
                index += 1
    print("")
    print("Enter an index to print the talk, or type b to return to main")
    user_index = input("Index: ")
    if(user_index.isdigit()):
        user_int = int(user_index)
        if user_int >= 0 and user_int <= index:
            printTalk(search_Talks[user_int], search_Conf[user_int])


def randomTalk(conferences):
    talk, conference = ca.randomTalk(conferences)
    printTalk(talk, conference)


def searchSpeaker(conferences):
    print("-Search By Speaker-")
    search_term = input("Enter a search term: ")
    terms = breakUpSearch(search_term)
    print("")
    index = 0
    search_Talks = []
    search_Conf = []

    for conf in conferences:
        for talk in conferences[conf].talks:
            result = [elem for elem in terms if(elem in talk.author.lower())]
            if len(result) == len(terms):
                search_Talks.append(talk)
                search_Conf.append(conf)
                print("<" + str(index) + ">: " + str(talk.title))
                print("\t" + str(talk.author))
                print("\t" + str(conf))
                print("")
                index += 1
    print("")
    print("Enter an index to print the talk, or type b to return to main")
    user_index = input("Index: ")
    if(user_index.isdigit()):
        user_int = int(user_index)
        if user_int >= 0 and user_int <= index:
            printTalk(search_Talks[user_int], search_Conf[user_int])


def searchContent(conferences, works, exact=False):
    wrapper = textwrap.TextWrapper()
    print("-Search By Content-")
    search_term = input("Enter a search term: ")
    terms = breakUpSearch(search_term)
    if exact:
        print("\"" + search_term.lower() + "\"")
    else:
        print(terms)
    print("")

    if exact:
        talk_paragraphs, search_Talks, search_Conf = ca.searchByContentExact(
            search_term, conferences)
    else:
        talk_paragraphs, search_Talks, search_Conf = ca.searchByContent(
            terms, conferences)
    for i in range(0, len(search_Talks)):
        print("<" + str(i) + ">: " + str(search_Talks[i].title))
        print("\t" + str(search_Talks[i].author))
        print("\t" + str(search_Conf[i]))
        wrapped_par = wrapper.wrap(text=talk_paragraphs[i])
        print('\t', end='')
        for line in wrapped_par:
            print(line)
        print("")

    if exact:
        search_verses, search_chapters = sa.searchByContentExact(
            search_term, works)
    else:
        search_verses, search_chapters = sa.searchByContent(terms, works)
    for i in range(0, len(search_verses)):
        print("<" + str(i + len(search_Talks)) + ">: ", end='')
        wrapped_par = wrapper.wrap(text=str(search_verses[i]))
        for line in wrapped_par:
            print(line)
        print("")

    print("")
    print("Enter an index to print the talk/chapter, or type b to return to main")
    user_index = input("Index: ")
    if(user_index.isdigit()):
        user_int = int(user_index)
        if user_int >= 0 and user_int < len(search_Talks):
            printTalk(search_Talks[user_int], search_Conf[user_int])
        elif user_int >= len(search_Talks) and user_int < len(search_Talks) + len(search_verses):
            printChapter(search_chapters[user_int - len(search_Talks)],
                         search_verses[user_int - len(search_Talks)].number)


def searchTitle(conferences):
    print("-Search By Title-")
    search_term = input("Enter a search term: ")
    terms = breakUpSearch(search_term)
    print("")
    index = 0
    search_Talks, search_Conf = ca.searchByTitle(terms, conferences)

    for i in range(0, len(search_Talks)):
        print("<" + str(i) + ">: " + str(search_Talks[i].title))
        print("\t" + str(search_Talks[i].author))
        print("\t" + str(search_Conf[i]))
    print("")
    print("Enter an index to print the talk, or type b to return to main")
    user_index = input("Index: ")
    if(user_index.isdigit()):
        user_int = int(user_index)
        if user_int >= 0 and user_int <= len(search_Talks):
            printTalk(search_Talks[user_int], search_Conf[user_int])


def wordOccurences(conferences):
    print("-Word Occurences-")
    print("Seperate seperate search terms by ' & ' (ex: joy & light & jesus)")
    user_input = input("Enter a word or phrase to search: ").lower()
    terms = user_input.split(' & ')
    print("---Searching all conferences for " + user_input + "---")
    occurenceList = []
    for term in terms:
        occurenceList.append(ca.wordOccurences(term, conferences))
    ca.plotOccurences(occurenceList, terms)
    print("")


def breakUpSearch(search_term):
    search_term = search_term.lower()
    terms = search_term.split()
    return terms


def printTalk(talk, conference):
    clearScreen()
    slow_read = True
    wrapper = textwrap.TextWrapper()

    print("(Enter p to print the whole talk at once)")
    print("")
    print(str(talk.title))
    print(str(talk.author))
    print(str(conference))
    print("")
    for paragraph in talk.paragraphs:
        wrapped_par = wrapper.wrap(text=paragraph)
        for line in wrapped_par:
            print(line)
        if slow_read:
            user_input = input("")
            if user_input.lower() == "p" or user_input.lower() == "q":
                slow_read = False
            elif user_input.lower() == "n":
                ref = str(talk.title) + ', ' + str(talk.author) + ": "
                ref += '\n' + str(paragraph)
                selectJournalToAddNote(ref)
        else:
            print("")


def printChapter(chapter, verseNumber=None):
    clearScreen()
    slow_read = False
    if(verseNumber == None):
        slow_read = True
    wrapper = textwrap.TextWrapper()

    print("(Enter p to print the whole chapter at once)")
    print("(Enter n to add a note ")
    print("")
    print(str(chapter.book) + " " + str(chapter.number))
    print("")
    for index, v in enumerate(chapter.verses):
        print(str(v.number) + " ", end='')
        wrapped_par = wrapper.wrap(text=v.verse)
        for line in wrapped_par:
            print(line)

        if(verseNumber == v.number):
            slow_read = True

        if(slow_read):
            user_input = input("")
            if(user_input.lower() == "p"):
                slow_read = False
            elif(user_input.lower() == "n"):
                selectJournalToAddNote(str(v))
        else:
            print("")


def browse(conferences, works):
    print("--Browse--")
    print("")
    print("<0>: General Conference")
    index = 1
    works_list = []
    for work in works:
        works_list.append(works[work])
        print("<" + str(index) + ">: " + str(work) + "")
        index += 1
    print("")
    user_index = input("Index: ")
    if(user_index.isdigit()):
        user_int = int(user_index)
        if user_int == 0:
            searchDate(conferences)
        elif user_int > 0 and user_int < len(works) + 1:
            browseWork(works_list[user_int - 1])
    return


def browseWork(work):
    clearScreen()
    print("--Browse " + str(work.title) + "--")
    print("")
    for i in range(0, len(work.books)):
        print("<" + str(i) + ">: " + str(work.books[i]))
    print("")
    user_index = input("Index: ")
    if(user_index.isdigit()):
        user_int = int(user_index)
        if user_int >= 0 and user_int < len(work.books):
            browseBook(work.books[user_int])


def browseBook(book):
    clearScreen()
    print("--Browse " + str(book) + "--")
    for i in range(0, len(book.chapters)):
        print("<" + str(i) + ">: " + str(book.chapters[i]))
    print("")
    user_index = input("Index: ")
    if(user_index.isdigit()):
        user_int = int(user_index)
        if user_int >= 0 and user_int < len(book.chapters):
            printChapter(book.chapters[user_int])


def viewAllJournals():
    journals = load_all_journals()
    journals_list = []
    index = 0

    clearScreen()

    for journal in journals:
        journals_list.append(journals[journal])
        print('<' + str(index) + '>: ' + str(journal))
        index += 1

    print()
    print('<' + str(index) + '>: ' + 'NEW JOURNAL')
    print()
    user_index = input('Index: ')
    if(user_index.isdigit()):
        user_int = int(user_index)
        if user_int >= 0 and user_int < len(journals_list):
            printJournal(journals_list[user_int])
        elif user_int == len(journals_list):
            makeNewJournal(journals)


def printJournal(journal: Journal):
    print()
    print()
    wrapper = textwrap.TextWrapper()
    clearScreen()
    print('--------- ' + journal.name + ' ---------')
    print(journal.description)
    print()
    for note in journal.notes:
        print()
        if(note.reference != None):
            wrapped_ref = wrapper.wrap(text=note.reference)
            for line in wrapped_ref:
                print(line)
        wrapped_content = wrapper.wrap(text=note.content)
        print()
        for line in wrapped_content:
            if note.reference != None:
                print('   ', end='')
            print(line)
        print()
        print('---')
        print()

    print('(add notes to journal, or just enter to return to menu)')
    print()
    user_input = 'a'
    while user_input != '':
        user_input = input(": ")
        if user_input != '':
            addNoteToJournal(journal, None, user_input=user_input)
        print()


def selectJournalToAddNote(ref: str):
    print()
    print('-------------------------')
    print('Add a New Note to Journal')
    print()
    journals = load_all_journals()
    journals_list = []
    index = 0

    for journal in journals:
        journals_list.append(journals[journal])
        print('<' + str(index) + '>: ' + str(journal))
        index += 1

    print()
    user_index = input('Index: ')
    if(user_index.isdigit()):
        user_int = int(user_index)
        if user_int >= 0 and user_int < len(journals_list):
            addNoteToJournal(journals_list[user_int], ref)
    print('-------------------------')
    print()


def addNoteToJournal(journal: Journal, reference, user_input=None):
    if user_input == None:
        user_input = input("New Note: ")
    new_note = Note(user_input, reference=reference)
    journal.add_note(new_note)
    save_journal(journal)


def makeNewJournal(journals):
    clearScreen()
    print('New Journal')
    print()
    name = input("Journal Name: ")
    if name in journals:
        print("Error, duplicate name")
        input()
        return
    description = input("Journal Description: ")
    new_journal = Journal(name, description)
    save_journal(new_journal)


if __name__ == "__main__":
    mainLoop()
