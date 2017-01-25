#!/usr/bin/python
# -*- coding: utf-8 -*-

from Cocoa import NSRunningApplication, NSApplicationActivateIgnoringOtherApps
import os
import Tkinter

from config_frame import ConfigFrame
from index_frame import IndexFrame
from word_frame import WordFrame
from test_frame import TestFrame
from result_frame import ResultFrame

from metrics import runtime


class Window(object):
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.root = Tkinter.Tk()
        self.root.title("French Verb Test")
        self.root.geometry("%dx%d" % (width, height))
        self.root.window = self
        self.background_color = "white"
        self.root.update()
        self.__index_frame = None
        self.__config_frame = None
        self.__word_frame = None
        self.__test_frame = None
        self.__result_frame = None

    @property
    def index_frame(self):
        if not self.__index_frame:
            self.__index_frame = IndexFrame(self.root)
        return self.__index_frame

    @property
    def config_frame(self):
        if not self.__config_frame:
            self.__config_frame = ConfigFrame(self.root)
        return self.__config_frame

    @property
    def word_frame(self):
        if not self.__word_frame:
            self.__word_frame = WordFrame(self.root)
        return self.__word_frame

    @property
    def test_frame(self):
        if not self.__test_frame:
            self.__test_frame = TestFrame(self.root)
        return self.__test_frame

    @property
    def result_frame(self):
        if not self.__result_frame:
            self.__result_frame = ResultFrame(self.root)
        return self.__result_frame

    def show(self):
        # Get focus of the window
        NSRunningApplication.runningApplicationWithProcessIdentifier_(os.getpid()).activateWithOptions_(
            NSApplicationActivateIgnoringOtherApps)
        self.root.mainloop()

    @runtime
    def switch_to_config(self):
        self.config_frame.show()
        self.root.update()
        #Tk.update_idletasks() maybe?

    @runtime
    def switch_to_index(self):
        self.index_frame.show()
        self.root.update()

    def switch_to_words(self):
        self.word_frame.show()
        self.root.update()

    def switch_to_test(self):
        self.test_frame.show()
        self.root.update()

    def switch_to_result(self, results):
        self.result_frame.set(results)
        self.result_frame.show()
        self.root.update()

    @runtime
    def init_menu(self):
        self.switch_to_index()


def main():
    window = Window(800, 600)
    window.init_menu()

    window.show()


if __name__ == "__main__":
    main()
