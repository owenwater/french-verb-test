#!/usr/bin/python

import os.path


class Cache(object):
    PATH = "cache/"

    def __init__(self, file, ext):
        self.file_name = file + "." + ext
        if not os.path.isdir(Cache.PATH):
            os.makedirs(Cache.PATH)

    @property
    def cache_path(self):
        return Cache.PATH + self.file_name

    @property
    def is_valid_cache(self):
        return os.path.isfile(self.cache_path) and os.path.getsize(self.cache_path) > 0

    def load_cache(self, handle):
        with open(self.cache_path) as fp:
            return handle(fp)

    def dump_cache(self, handle):
        with open(self.cache_path, "wb") as fp:
            return handle(fp)
