
class Verse:
    def __init__(self, book, chapter, number, verse):
        self.book = book
        self.chapter = chapter
        self.number = number
        self.verse = verse

    def __str__(self):
        return str(self.book) + " " + str(self.chapter.number) + ":" + str(self.number) + "\n" + str(self.verse)


class Chapter:
    def __init__(self, book, number):
        self.book = book
        self.number = number
        self.verses = []

    def addVerse(self, verse):
        self.verses.append(verse)

    def __str__(self):
        return str(self.book) + " " + str(self.number)


class Book:
    def __init__(self, title):
        self.title = title
        self.chapters = []

    def addChapter(self, chapter):
        self.chapters.append(chapter)

    def __str__(self):
        return str(self.title)

class StandardWork:
    def __init__(self, title):
        self.title = title
        self.books = []

    def addBook(self, book):
        self.books.append(book)

    def __str__(self):
        return str(self.title)
