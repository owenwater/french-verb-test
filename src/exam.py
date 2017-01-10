#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import json
import os

from verb import VerbFactory, Verb


class Exam(object):
    random.seed()
    WORDS_PATH = "../config/words"
    EXAM_PATH = "../config/exam.json"
    DEFAULT_EXAM_CONFIG = {
        "mood": "random",    # random, all or the list of mood name.
        "mood_num": 3,
        "tense": "random",    # random, all or the list of tense name.
        "tense_num": 3,
        "word": "random",
        "word_num": 10,
        "type": "fit",    # fit or all.
    }
    MOODS = {u"Indicatif", u"Conditionnel", u"Subjonctif", u"Impératif", u"Infinitif", u"Participe", u"Gérondif"}
    TENSES = {
        u"Présent", u"Passé composé", u"Imparfait", u"Plus-que-parfait", u"Passé simple", u"Passé antérieur",
        u"Futur simple", u"Futur antérieur"
    }

    def __init__(self):
        with open(Exam.WORDS_PATH) as fp:
            words = {word.strip() for word in fp.readlines()}
        verb_factory = VerbFactory(words)
        self.verbs = verb_factory.load_all()
        if not self.load_config():
            self.config = Exam.DEFAULT_EXAM_CONFIG
            self.dump_config()

    def load_config(self):
        if not os.path.isfile(Exam.EXAM_PATH):
            return False
        try:
            with open(Exam.EXAM_PATH) as fp:
                self.config = json.load(fp)
        except ValueError:
            return False
        return True

    def dump_config(self):
        with open(Exam.EXAM_PATH, "w") as fp:
            json.dump(self.config, fp, indent=2, sort_keys=True)

    def choose_from_list(self, type, type_num, items):
        """ Pick item from the list based on the config.
        """
        if self.config[type] == "all":
            return items
        elif self.config[type] == "random":
            if len(items) < self.config[type_num]:
                return items
            return random.sample(items, self.config[type_num])
        else:
            return self.config[type]

    def choose_all_list(self, choose_verb=True):
        """ Pick the list mood, tense and words from the avaiable list based the the config.
            Verb will be choosed iff |choose_verb| is True.
        """
        self.choosed_moods = self.choose_from_list('mood', 'mood_num', Exam.MOODS)
        self.choosed_tenses = self.choose_from_list('tense', 'tense_num', Exam.TENSES)
        if choose_verb:
            self.choosed_verbs = self.choose_from_list('word', 'word_num', self.verbs)

    @property
    def is_fit(self):
        return self.config['type'] == "fit"

    def generate_tests(self):
        """generate test cases based on the config.
        """
        exam.choose_all_list()
        self.tests = {}
        for verb in self.choosed_verbs:
            if self.is_fit:
                num_of_spaces = len(verb.word) + random.randint(10, 15)
            else:
                num_of_spaces = len(verb.word) + random.randint(25, 30)
            test_mood = {}
            for mood in self.choosed_moods:
                test_tense = {}
                for tense in self.choosed_tenses:
                    test_words = []
                    if mood in verb.data and tense in verb.data[mood]:
                        for words in verb.data[mood][tense]:
                            test_word = ""
                            if self.is_fit:
                                test_word = verb.print_words(words, var=lambda w: "_" * num_of_spaces)
                            else:
                                test_word = "_" * num_of_spaces
                            test_words.append(test_word)
                        test_tense[tense] = test_words
                if test_tense:
                    test_mood[mood] = test_tense
            if test_mood:
                self.tests[verb] = test_mood

    def check_answer(self, actual_answer):
        pass


if __name__ == "__main__":
    exam = Exam()
    exam.generate_tests()
    print exam.tests
    if not exam.tests:
        print exam.choosed_moods
        print exam.choosed_tenses
