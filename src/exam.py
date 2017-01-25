#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

from verb import VerbFactory, Verb
from exam_config import ExamConfig


class Exam(object):
    MOOD = "mood"
    TENSE = "tense"
    WORDS = "words"
    VERB = "verb"
    BLANK = "_"

    def __init__(self):
        random.seed()
        self.config = ExamConfig.create()
        verb_factory = VerbFactory(self.config.words)
        self.verbs = verb_factory.load_all()

    def choose_from_list(self, (type, type_num, type_list), items):
        """ Pick item from the list based on the config.
        """
        if self.config[type] == "all":
            return items
        elif self.config[type] == "random":
            if len(items) < self.config[type_num]:
                return items
            return random.sample(items, self.config[type_num])
        else:
            return self.config[type_list]

    def choose_all_list(self, choose_verb=True):
        """ Pick the list mood, tense and words from the avaiable list based the the config.
            Verb will be choosed iff |choose_verb| is True.
        """
        self.choosed_moods = self.choose_from_list(ExamConfig.MOOD_KEY_WORD, ExamConfig.MOODS)
        self.choosed_tenses = self.choose_from_list(ExamConfig.TENSE_KEY_WORD, ExamConfig.TENSES)
        if choose_verb:
            self.choosed_verbs = self.choose_from_list(ExamConfig.WORD_KEY_WORD, self.verbs)

    @property
    def is_fill_blank(self):
        return self.config[ExamConfig.FILL_BLANK]

    def generate_tests(self):
        """generate test cases based on the config.
        """
        self.choose_all_list()
        self.tests = []
        for verb in self.choosed_verbs:
            space = lambda w: Exam.BLANK
            if self.is_fill_blank:
                num_of_spaces = len(verb.word) + random.randint(10, 15)
            else:
                num_of_spaces = len(verb.word) + random.randint(25, 30)
            test_mood = {}
            for mood in self.choosed_moods:
                test_tense = {}
                for tense in self.choosed_tenses:
                    test_words = []
                    if mood in verb and tense in verb[mood]:
                        for words in verb[mood][tense]:
                            test_word = ""
                            if self.is_fill_blank:
                                test_word = Verb.print_words(words, var=space)
                            else:
                                test_word = Verb.print_words(words, var=space, const=space)
                            test_words.append(test_word)
                            self.tests.append({
                                Exam.MOOD: mood,
                                Exam.TENSE: tense,
                                Exam.WORDS: test_words,
                                Exam.VERB: verb
                            })
        random.shuffle(self.tests)
        self.tests = self.tests[:self.config[ExamConfig.TEST_NUM]]

    @classmethod
    def check_answer(cls, expected, actual):
        """Check the actual answer is correct
           actual: a dict {
            "mood": mood
            "tense": tense
            "words" : [list of words]
           }
        """
        expected_words = [Verb.print_words(word) for word in expected[actual['mood']][actual['tense']]]
        if expected_words != actual["words"]:
            return False, expected_words, actual["words"]
        return True, [], []


if __name__ == "__main__":
    exam = Exam()
    exam.generate_tests()
    print exam.tests
    if not exam.tests:
        print exam.choosed_moods
        print exam.choosed_tenses

    #for test in exam.tests:
    #ret, expect, actual = exam.check_answer(test, {
    #"mood": u"Indicatif",
    #"tense": u"Futur antérieur",
    #"words":
    #[u"j'aurai été", u"tu auras été", u"il aura été", u"nous aurons été", u"vous aurez été", u"ils auront été"]
    #})
    #print "Correct" if ret else "Wrong"
