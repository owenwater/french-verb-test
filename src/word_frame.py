#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter

from exam_config import ExamConfig


class WordFrame(Tkinter.Frame):
    def __init__(self, master):
        Tkinter.Frame.__init__(self, master)

        self.__words_list_widget = None
        self.__back_button = None
        self.__words = None
        self.sub_init = False

    @property
    def words(self):
        if self.__words == None:
            self.config = ExamConfig.create()
            self.__words = sorted(list(self.config.words))
        return self.__words

    @property
    def words_list_widget(self):
        if not self.__words_list_widget:
            self.__words_list_widget = Tkinter.Listbox(self, selectmode=Tkinter.BROWSE)
            for word in self.words:
                self.__words_list_widget.insert(Tkinter.END, word)
        return self.__words_list_widget

    @property
    def back_button(self):
        if not self.__back_button:
            self.__back_button = Tkinter.Button(self, text="Back", command=self.on_back)
        return self.__back_button

    def show(self):
        self.place(relx=.5, rely=.1)
        if self.sub_init:
            return
        self.words_list_widget.pack(side=Tkinter.TOP, pady=10)
        self.back_button.pack(side=Tkinter.TOP, pady=10)

        self.sub_init = True

    def on_back(self):
        self.place_forget()
        self.master.window.switch_to_index()
