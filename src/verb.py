#!/usr/bin/python

from bs4 import BeautifulSoup
import json

from cache import Cache
from gateway import Gateway


class bcolors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    END = '\033[0m'


class Verb(object):
    VAR = "var"
    CONST = "const"

    def __init__(self, word):
        self.word = word
        self.gateway = Gateway(word)
        self.cache = Cache(word, "json")

    def load(self, ignore_cache=False):
        """Get all verb's moods from local cache if exist and |ignore_cache| is false.
           Otherwise, parse it from the webpage.
        """
        if not ignore_cache and self.cache.is_valid_cache:
            self.data = self.cache.load_cache(lambda fp: json.load(fp))
            return True
        self.page = self.gateway.fetch()
        if not self.page:
            return False
        self.data = self.parse()
        self.cache.dump_cache(lambda fp: json.dump(self.data, fp))
        return True

    def parse(self):
        """parse the html page and return dict of the words
        """
        html = BeautifulSoup(self.page.decode('iso8859-15'), "html.parser")
        tag = html.find("h2", class_="mode")
        mood = ""
        tenses = {}
        moods = {}
        while tag:
            if tag.name == u"h2" and tag.attrs.get("class", [None])[0] == u"mode":
                if tenses and mood:
                    moods[mood] = tenses
                    tenses = {}
                mood = tag.next.next.strip()
            elif tag.name == u"div" and tag.attrs.get("class", [None])[0] == u"tempstab":
                tense = tag.find("h3", class_="tempsheader").next.strip()
                content = tag.find("div", class_="tempscorps")
                words = []
                word = []
                for c in content:
                    if c.name == u"b":
                        word.append([c.next, Verb.VAR])
                    elif c.name == u"br":
                        word[0][0] = word[0][0].lstrip()
                        word[-1][0] = word[-1][0].rstrip()
                        words.append(word)
                        word = []
                    else:
                        word.append([c, Verb.CONST])
                tenses[tense] = words
            tag = tag.find_next_sibling()
        if tenses and mood:
            moods[mood] = tenses
        return moods

    @staticmethod
    def print_words(words, const=None, var=None):
        s = ""
        for word in words:
            if word[1] == Verb.VAR and var:
                s += var(word[0])
            elif word[1] == Verb.CONST and const:
                s += const(word[0])
            else:
                s += word[0]
        return s

    def __unicode__(self):
        str = u""
        for mood in self.data:
            str += mood + u":\n"
            for tense in self.data[mood]:
                str += u"\t" + tense + ":\n"
                for words in self.data[mood][tense]:
                    str += u"\t\t" + Verb.print_words(words, var=lambda w: bcolors.RED + w + bcolors.END) + u"\n"
            str += u"\n"
        return str

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __getitem__(self, key):
        return self.data[key]

    def __len__(self):
        return len(self.data)

    def has_key(self, key):
        return self.data.has_key(key)

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return self.data.items()

    def __contains__(self, item):
        return item in self.data

    def __iter__(self):
        return iter(self.data)


class VerbFactory(object):
    def __init__(self, words):
        """ Init VerbFactory with the set of words. 
        """
        self.verbs = {Verb(word) for word in words}

    def load_all(self):
        """ Load all verbs' data from cache or web and return them
        """
        for verb in self.verbs:
            verb.load()
        return self.verbs


if __name__ == "__main__":
    path = "../config/words"
    with open(path) as fp:
        words = {word.strip() for word in fp.readlines()}
    verb_factory = VerbFactory(words)
    verbs = verb_factory.load_all()
    for verb in verbs:
        print bcolors.PINK + verb.word + bcolors.END
        print str(verb)
