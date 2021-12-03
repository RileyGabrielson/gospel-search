from scripture import Verse, Chapter, Book, StandardWork
import pickle
from collections import Counter
import os

def loadWork(fileName):
    work = None
    with open(fileName, 'rb') as file:
        work = pickle.load(file)
    return work

def loadAllWorks():
    works = dict()
    for root, dirs, files in os.walk("./scriptures", topdown=False):
        for file in files:
            if file.endswith(".pickle"):
                newWork = loadWork(os.path.join(root, file))
                works[newWork.title] = newWork
    return works

def searchByContent(terms, works):
    search_verses = []
    search_chapters = []

    for work in works:
        for book in works[work].books:
            for chapter in book.chapters:
                for verse in chapter.verses:
                    result = [elem for elem in terms if(elem.lower() in str(verse).lower())]
                    if len(result) == len(terms):
                        search_verses.append(verse)
                        search_chapters.append(chapter)

    return search_verses, search_chapters

def searchByContentExact(phrase, works):
    search_verses = []
    search_chapters = []
    phrase = phrase.lower()

    for work in works:
        for book in works[work].books:
            for chapter in book.chapters:
                for verse in chapter.verses:
                    if phrase in str(verse).lower():
                        search_verses.append(verse)
                        search_chapters.append(chapter)

    return search_verses, search_chapters
