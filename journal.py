import pickle
import os
from collections import OrderedDict


class Note:
    def __init__(self, content, reference=None):
        self.reference = reference
        self.content = content


class Journal:
    def __init__(self, name, description=None):
        self.name = name
        self.notes = []
        self.description = description

    def add_note(self, note: Note):
        self.notes.append(note)


def save_journal(journal: Journal):
    with open("journals/" + journal.name + '.pickle', 'wb') as output:
        pickle.dump(journal, output, pickle.HIGHEST_PROTOCOL)


def load_all_journals():
    journals = dict()
    for root, _, files in os.walk("./journals", topdown=False):
        for file in files:
            if file.endswith(".pickle"):
                newJournal = load_journal(os.path.join(root, file))
                journals[newJournal.name] = newJournal

    return OrderedDict(sorted(journals.items()))


def load_journal(fileName):
    conference = None
    with open(fileName, 'rb') as file:
        conference = pickle.load(file)
    return conference
