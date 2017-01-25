#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter

from exam import Exam


class TitleFrame(Tkinter.Frame):
    def __init__(self, master, mood, tense, cnt):
        Tkinter.Frame.__init__(self, master)
        self.cnt = cnt
        self.mood = mood
        self.tense = tense

        self.__mood_label = None
        self.__tense_label = None
        self.__cnt_label = None

    @property
    def cnt_label(self):
        if not self.__cnt_label:
            self.__cnt_label = Tkinter.Label(self, text=self.cnt)
        return self.__cnt_label

    @property
    def mood_label(self):
        if not self.__mood_label:
            self.__mood_label = Tkinter.Label(self, text=self.mood)
        return self.__mood_label

    @property
    def tense_label(self):
        if not self.__tense_label:
            self.__tense_label = Tkinter.Label(self, text=self.tense)
        return self.__tense_label

    def show(self):
        self.pack(pady=20, side=Tkinter.TOP)
        self.cnt_label.pack(side=Tkinter.TOP)
        self.mood_label.pack(pady=30, padx=100, side=Tkinter.LEFT)
        self.tense_label.pack(pady=30, padx=100, side=Tkinter.RIGHT)


class WordFrame(Tkinter.Frame):
    def __init__(self, master, word):
        Tkinter.Frame.__init__(self, master)
        self.word = word
        self.entries = []

    def show(self):
        self.pack(side=Tkinter.TOP)
        first = True
        for part in self.word.split(Exam.BLANK):
            if part != "":
                Tkinter.Label(self, text=part).pack(side=Tkinter.LEFT)
            if first:
                first = False
            else:
                entry = Tkinter.Entry(self, width=30)
                entry.pack(side=Tkinter.LEFT)
                self.entries.append(entry)

    def get(self):
        for entry in self.entries:
            self.word = self.word.replace(Exam.BLANK, entry.get(), 1)
        return self.word


class ButtonFrame(Tkinter.Frame):
    def __init__(self, master, is_last):
        Tkinter.Frame.__init__(self, master)
        self.is_last = is_last
        self.__next_button = None
        self.__abort_button = None

    @property
    def next_button(self):
        if not self.__next_button:
            self.__next_button = Tkinter.Button(self, text="Finish" if self.is_last else "Next", command=self.on_next)
        return self.__next_button

    @property
    def abort_button(self):
        if not self.__abort_button:
            self.__abort_button = Tkinter.Button(self, text="Abort", command=self.on_abort)
        return self.__abort_button

    def show(self):
        self.pack(side=Tkinter.TOP)
        self.next_button.pack(padx=100, side=Tkinter.RIGHT)
        self.abort_button.pack(padx=100, side=Tkinter.LEFT)

    def on_next(self):
        self.master.next_test()

    def on_abort(self):
        self.master.finish_test()


class TestFrame(Tkinter.Frame):
    def __init__(self, master):
        Tkinter.Frame.__init__(self, master)
        self.exam = None
        self.words = []

    def show(self):
        if not self.exam:    #TODO: make it as a property
            self.exam = Exam()
        cnt = 0
        while True:
            self.exam.generate_tests()    #TODO: maybe we need a loading progress bar and do this in an separate thread
            if len(self.exam.tests) > 0 or cnt > 20:
                break
            cnt += 1

        self.index = 0
        self.num_of_tests = len(self.exam.tests)
        if self.num_of_tests == 0:
            return    #TODO: show warning message and return button instread
        self.show_test()

    def show_test(self):
        self.pack()
        self.words = []
        test = self.exam.tests[self.index]
        cnt_str = "%d/%d" % (self.index + 1, self.num_of_tests)
        TitleFrame(self, test[Exam.MOOD], test[Exam.TENSE], cnt_str).show()
        for word in self.exam.tests[self.index][Exam.WORDS]:
            word = WordFrame(self, word)
            word.show()
            self.words.append(word)
        ButtonFrame(self, (self.index == self.num_of_tests - 1)).show()
        self.update()

    def next_test(self):
        answers = []
        for word in self.words:
            answers.append(word.get())
        self.exam.tests[self.index][Exam.WORDS] = answers

        self.index += 1
        if self.index >= self.num_of_tests:
            self.finish_test()
        else:
            for widget in self.winfo_children():
                widget.destroy()
            self.show_test()

    def finish_test(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.pack_forget()
        if self.index > 0:
            self.master.window.switch_to_result(self.exam.tests[:self.index])
        else:
            self.master.window.switch_to_index()
