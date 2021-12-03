import pickle
from scripture import Verse, Chapter, Book, StandardWork

def parseWorkToFile(fileName, workName):
    work = StandardWork(workName)
    curBook = Book("None")
    curChapter = Chapter(curBook, 0)
    abbreviations = getAbbrev("scripture_source/contents.txt")

    file = open(fileName, "r", errors="ignore")
    content = file.read()
    contents = content.split('\n')
    for v in contents:
        if v != '':
            verseBook = v[:3]
            if(abbreviations[verseBook] != curBook.title):
                curBook = Book(abbreviations[verseBook])
                work.addBook(curBook)

            colonIndex = v.index(':', 0, 9)
            verseChapter = v[4:colonIndex]
            if (verseChapter != curChapter.number) or (curBook.title != curChapter.book.title):
                curChapter = Chapter(curBook, verseChapter)
                curBook.addChapter(curChapter)

            spaceIndex = v.index(' ', colonIndex, 15)
            verseNumber = v[colonIndex+1:spaceIndex]
            verse = Verse(curBook, curChapter, verseNumber, v[spaceIndex+1:])
            curChapter.addVerse(verse)

    with open("scriptures/" + workName + '.pickle', 'wb') as output:
        pickle.dump(work, output, pickle.HIGHEST_PROTOCOL)


def importBibleToFile(fileName):
    work = StandardWork("Bible (KJV)")
    curBook = Book("None")
    curChapter = Chapter(curBook, 0)
    abbreviations = getAbbrev("scripture_source/contents.txt")

    file = open(fileName, "r")
    contents = file.read().split('\n')

    for v in contents:
        if v != '':
            barIndex = v.index('|')
            verseBook = v[:barIndex].upper()
            if(abbreviations[verseBook] != curBook.title):
                curBook = Book(abbreviations[verseBook])
                work.addBook(curBook)

            barIndex2 = v.index('|', barIndex + 1)
            verseChapter = v[barIndex+1:barIndex2]
            if (verseChapter != curChapter.number) or (curBook.title != curChapter.book.title):
                curChapter = Chapter(curBook, verseChapter)
                curBook.addChapter(curChapter)

            barIndex3 = v.index('|', barIndex2 + 1)
            verseNumber = v[barIndex2+1:barIndex3]
            verse = Verse(curBook, curChapter, verseNumber, v[barIndex3+2:-1])
            curChapter.addVerse(verse)

    with open("scriptures/" + "KingJamesBible" + '.pickle', 'wb') as output:
        pickle.dump(work, output, pickle.HIGHEST_PROTOCOL)



def getAbbrev(fileName):
    abbreviations = dict()

    file = open(fileName, "r")
    contents = file.read().split()
    for i in range(int(len(contents) / 2)):
        abbreviations[contents[(2*i)+1]] = contents[2*i]
    return abbreviations

if __name__ == "__main__":
    parseWorkToFile("scripture_source/DoctrineAndCovenants.txt", "Doctrine And Covenants")
    #importBibleToFile("scripture_source/KingJamesBible.txt")

    with open("scriptures/KingJamesBible.pickle", 'rb') as file:
        bible = pickle.load(file)
        print(bible.books[0].chapters[0].verses[0].verse)
