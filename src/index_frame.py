#!/usr/bin/python

import Tkinter

from metrics import runtime


def test():
    print "test"


class IndexFrame(Tkinter.Frame):
    def __init__(self, master):
        Tkinter.Frame.__init__(self, master)
        self.sub_init = False

    @property
    def button_width(self):
        return self.master.winfo_width() / 50

    @property
    def button_pad(self):
        return self.master.winfo_width() / 40

    def show(self):
        self.place(relx=.5, rely=.43, anchor="c")
        if self.sub_init:
            return
        self.config_button = Tkinter.Button(
            self, text="Config", command=self.on_config_button_pressed, width=self.button_width)
        self.test_button = Tkinter.Button(
            self, text="Test", command=self.on_test_button_pressed, width=self.button_width)
        self.word_button = Tkinter.Button(
            self, text="Word", command=self.on_word_button_pressed, width=self.button_width)

        self.config_button.pack(side=Tkinter.LEFT, padx=self.button_pad)
        self.test_button.pack(side=Tkinter.RIGHT, padx=self.button_pad)
        self.word_button.pack(side=Tkinter.LEFT, padx=self.button_pad)
        self.sub_init = True

    def on_config_button_pressed(self):
        self.place_forget()
        self.master.window.switch_to_config()

    def on_word_button_pressed(self):
        self.place_forget()
        self.master.window.switch_to_words()

    def on_test_button_pressed(self):
        self.place_forget()
        self.master.window.switch_to_test()
