#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler
import urllib2
import sys

from cache import Cache


class Gateway(object):
    URL = u"http://la-conjugaison.nouvelobs.com/du/verbe/%s.php"

    def __init__(self, word):
        self.word = word
        self.cache = Cache(word, "html")

    def fetch(self, ignore_cache=False):
        """ fetch the webpage from local cache if exist and |ignore_cache| is false.
            Otherwise, read from the website and cache result locally.
        """
        if not ignore_cache and self.cache.is_valid_cache:
            return self.cache.load_cache(lambda fp: "".join(fp.readlines()))

        url = Gateway.URL % (self.word)
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError as e:
            sys.stderr.write(str(e.code) + ": ")
            sys.stderr.write(", ".join(BaseHTTPRequestHandler.responses[e.code]))
            sys.stderr.write(".\n")
            return ""
        page = response.read()
        self.cache.dump_cache(lambda fp: fp.write(page))
        return page
