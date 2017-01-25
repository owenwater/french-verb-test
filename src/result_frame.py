#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter
import tkFileDialog

from exam import Exam
from test_frame import TitleFrame


class ButtonFrame(Tkinter.Frame):
    def __init__(self, master, is_first, is_last):
        Tkinter.Frame.__init__(self, master)
        self.is_first = is_first
        self.is_last = is_last
        self.__back_button = None
        self.__next_button = None
        self.__end_button = None
        self.__save_button = None

    @property
    def back_button(self):
        if not self.__back_button:
            state = Tkinter.DISABLED if self.is_first else Tkinter.NORMAL
            self.__back_button = Tkinter.Button(self, text="Previous", state=state, command=self.on_back)
        return self.__back_button

    def on_back(self):
        self.master.previous_wrong_answer()

    @property
    def next_button(self):
        if not self.__next_button:
            state = Tkinter.DISABLED if self.is_last else Tkinter.NORMAL
            self.__next_button = Tkinter.Button(self, text="Next", state=state, command=self.on_next)
        return self.__next_button

    def on_next(self):
        self.master.next_wrong_answer()

    @property
    def end_button(self):
        if not self.__end_button:
            self.__end_button = Tkinter.Button(self, text="End", command=self.on_end)
        return self.__end_button

    def on_end(self):
        self.master.on_finish()

    @property
    def save_button(self):
        if not self.__save_button:
            self.__save_button = Tkinter.Button(self, text="Save Result", command=self.on_save)
        return self.__save_button

    def on_save(self):
        self.master.on_save()

    def show(self):
        self.pack(pady=30, side=Tkinter.TOP)
        self.back_button.pack(padx=50, side=Tkinter.LEFT)
        self.next_button.pack(padx=50, side=Tkinter.LEFT)
        self.save_button.pack(padx=50, side=Tkinter.LEFT)
        self.end_button.pack(padx=50, side=Tkinter.LEFT)


class WordFrame(Tkinter.Frame):
    def __init__(self, master, expect, actual, is_red=False, is_title=False):
        Tkinter.Frame.__init__(self, master)
        self.is_red = is_red
        self.is_title = is_title
        self.expect = expect
        self.actual = actual

    def show(self):
        pady = 20 if self.is_title else 0
        self.pack(pady=pady, side=Tkinter.TOP)
        color = "red" if self.is_red else "black"
        Tkinter.Label(self, text=self.expect, fg=color).pack(side=Tkinter.LEFT, padx=100)
        Tkinter.Label(self, text=self.actual, fg=color).pack(side=Tkinter.RIGHT, padx=100)


class ResultFrame(Tkinter.Frame):
    def __init__(self, master):
        Tkinter.Frame.__init__(self, master)

    @property
    def score_label(self):
        if not self.__score_label:
            self.__score_label = Tkinter.Label

    def set(self, results):
        self.total = len(results)
        self.correct = 0
        self.wrong = []
        for result in results:
            is_correct, expect, actual = Exam.check_answer(result[Exam.VERB], result)
            if is_correct:
                correct += 1
            else:
                self.wrong.append((expect, actual, result))
        self.__score_label = None

    def show(self):
        if self.total == self.correct:
            self.place(relx=.5, rely=.43, anchor="c")
            Tkinter.Label(self, text=u"Félicitations, toutes les réponses sont correctes.").pack(side=Tkinter.TOP)
            Tkinter.Button(self, text=u"End", command=self.on_finish).pack(side=Tkinter.TOP)
        else:
            self.pack()
            self.index = 0
            self.show_wrong_answer()

    def show_wrong_answer(self):
        cnt_str = "Score: %d/%d, #%d" % (self.correct, self.total, self.index + 1)
        expect, actual, result = self.wrong[self.index]
        TitleFrame(self, result[Exam.MOOD], result[Exam.TENSE], cnt_str).show()
        WordFrame(self, u"Bonne réponse", u"Ta Réponse", is_title=True).show()
        for expect_word, actual_word in zip(expect, actual):
            WordFrame(self, expect_word, actual_word, is_red=(expect_word != actual_word)).show()
        ButtonFrame(self, self.index == 0, self.index == self.total - self.correct - 1).show()
        self.update()

    def next_wrong_answer(self):
        self.reset()
        self.index += 1
        self.show_wrong_answer()

    def previous_wrong_answer(self):
        self.reset()
        self.index -= 1
        self.show_wrong_answer()

    def on_finish(self):
        self.reset()
        self.place_forget()
        self.pack_forget()
        self.master.window.switch_to_index()

    def on_save(self):
        file_name = tkFileDialog.asksaveasfilename(defaultextension=".txt")
        if file_name:
            with open(file_name, "w") as fp:
                for expected, actual, result in self.wrong:
                    title = u"%s: %s, %s:\n" % (result[Exam.VERB].word, result[Exam.MOOD], result[Exam.TENSE])
                    fp.write(title.encode('utf8'))
                    for expected_word in expected:
                        words = expected_word + u"\n"
                        fp.write(words.encode('utf8'))
                    fp.write(u"\n")

    def reset(self):
        for widget in self.winfo_children():
            widget.destroy()
