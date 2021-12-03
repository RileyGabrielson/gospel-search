import requests
from bs4 import BeautifulSoup


class Conference:
    def __init__(self, name):
        self.talks = []
        self.name = name

    def __str__(self):
        return self.name

    def addTalk(self, talk):
        self.talks.add(talk)

    def parseByURL(self, url):
        self.talks.clear()
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='content')
        sessions = results.findAll('li')
        for session in sessions:
            sessionUL = session.find('ul')
            if sessionUL != None:
                talkLinks = sessionUL.findAll('a')
                for talkLink in talkLinks:
                    if 'session' not in str(talkLink['href']).lower():
                        newTalk = Talk(
                            "https://www.churchofjesuschrist.org" + talkLink['href'])
                        self.talks.append(newTalk)

    def listTalks(self):
        string = ""
        for talk in self.talks:
            string += str(talk)
            string += '\n'
        return string


class Talk:
    def __init__(self, url=None):
        self.paragraphs = []
        self.title = "EMPTY TITLE"
        self.author = "EMPTY AUTHOR"
        if url != None:
            self.parseByURL(url)

    def __str__(self):
        return self.author + ": " + self.title

    def __hash__(self):
        return (len(self.author) + 13) | len(self.title) | len(self.paragraphs[0])

    def simplifyAuthor(self, author):
        if author[:3] == "By ":
            author = author[3:]
        if len(author) > 13:
            if author[:13] == "Presented by ":
                author = author[13:]
        if len(author) > 8:
            if author[:6] == "Elder ":
                author = author[6:]
            if author[:7] == "Bishop ":
                author = author[7:]
        if len(author) > 10:
            if author[:10] == "President ":
                author = author[10:]
        return author

    def parseByURL(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find(id="title1")
        if title == None:
            title = soup.find(id="p1")
        if title == None:
            self.title = "Unnamed"
        else:
            self.title = title.text

        # Only Parse Conference talks (see https://www.churchofjesuschrist.org/study/general-conference/2020/10/33video?lang=eng)
        if "Video: " in self.title:
            print("Did not parse " + self.title + ", suspected video only")
            return

        subtitle = soup.find(id="subtitle1")
        if subtitle != None:
            self.title += " " + subtitle.text
        author = soup.find("p", {"class", "author-name"})
        if author == None:
            author = soup.find(id="p1")
        if author == None:
            author = soup.find(id="author1")
        if author == None:
            self.author = "No Author"
        else:
            self.author = self.simplifyAuthor(author.text)

        results = soup.find(id="content")
        if results != None:
            body = results.find("div", class_="body-block")
            text_blocks = body.find_all("p")
            for paragraph in text_blocks:
                self.paragraphs.append(paragraph.text)

        print(str(self))


# Role of Bishop, October 1979 Marion G Romney missing name and title
