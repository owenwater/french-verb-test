#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os


class ExamConfig(object):
    @classmethod
    def create(cls):
        if not hasattr(cls, "__instance") or not cls.__instnace:
            cls.__instance = ExamConfig()
        return cls.__instance

    MOOD = "mood"
    MOOD_NUM = "mood_num"
    MOOD_LIST = "mood_list"
    MOOD_KEY_WORD = (MOOD, MOOD_NUM, MOOD_LIST)

    TENSE = "tense"
    TENSE_NUM = "tense_num"
    TENSE_LIST = "tense_list"
    TENSE_KEY_WORD = (TENSE, TENSE_NUM, TENSE_LIST)

    WORD = "word"
    WORD_NUM = "word_num"
    WORD_LIST = "word_list"
    WORD_KEY_WORD = (WORD, WORD_NUM, WORD_LIST)

    TEST_NUM = "test_num"

    FILL_BLANK = "fill_blank"

    EXAM_PATH = "config/exam.json"
    DEFAULT_EXAM_CONFIG = {
        "mood": "random",    # random, all or the list of mood name.
        "mood_num": 3,
        "tense": "random",    # random, all or the list of tense name.
        "tense_num": 3,
        "word": "random",
        "word_num": 10,
        "test_num": 20,
        "fill_blank": True,    # fill_blank or all.
    }
    MOODS = {u"Indicatif", u"Conditionnel", u"Subjonctif", u"Impératif", u"Infinitif", u"Participe", u"Gérondif"}
    TENSES = {
        u"Présent", u"Passé composé", u"Imparfait", u"Plus-que-parfait", u"Passé simple", u"Passé antérieur",
        u"Futur simple", u"Futur antérieur"
    }

    WORDS_PATH = "config/words"

    @staticmethod
    def moods():
        return sorted(list(ExamConfig.MOODS))

    @staticmethod
    def tenses():
        return sorted(list(ExamConfig.TENSES))

    def __init__(self):
        if not self.load_config():
            self.config = ExamConfig.DEFAULT_EXAM_CONFIG
            self.dump_config()

        if not self.load_words():
            self.words = []

    def load_config(self):
        if not os.path.isfile(ExamConfig.EXAM_PATH):
            return False
        try:
            with open(ExamConfig.EXAM_PATH) as fp:
                self.config = json.load(fp)
        except ValueError:
            return False
        return True

    def dump_config(self):
        with open(ExamConfig.EXAM_PATH, "w") as fp:
            json.dump(self.config, fp, indent=2, sort_keys=True)

    def load_words(self):
        if not os.path.isfile(ExamConfig.WORDS_PATH):
            return False
        with open(ExamConfig.WORDS_PATH) as fp:
            self.words = {word.strip() for word in fp.readlines()}
        return True

    def __getitem__(self, key):
        return self.config[key]

    def __contains__(self, key):
        return key in self.config

    def has_key(self, key):
        return self.config.has_key(key)

    def __setitem__(self, key, value):
        self.config[key] = value


if __name__ == "__main__":
    print ExamConfig.moods()
    print ExamConfig.tenses()
