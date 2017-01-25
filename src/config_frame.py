#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter

from exam_config import ExamConfig
from metrics import runtime


class ListChooseFrame(Tkinter.Frame):
    OPTIONS = ('All', 'Random', 'Custom')

    def __init__(self, master, type, items, default_mode=1, default_num=3, default_list=[]):
        Tkinter.Frame.__init__(self, master)
        self.type = type
        self.items = items
        self.default_mode = ListChooseFrame.OPTIONS.index(default_mode.capitalize())
        self.default_num = default_num
        self.default_list = [items.index(item) for item in default_list]

        self.__label_widget = None
        self.__selector_widget = None
        self.__num_pad_widget = None
        self.__item_list_widget = None

        self.__current_second_widget = None

    @property
    def label_widget(self):
        if not self.__label_widget:
            self.__label_widget = Tkinter.Label(self, text=self.type)
        return self.__label_widget

    @property
    def selector_widget(self):
        if not self.__selector_widget:
            self.__selector_widget = Tkinter.OptionMenu(
                self,
                Tkinter.StringVar(value=ListChooseFrame.OPTIONS[self.default_mode]),
                *ListChooseFrame.OPTIONS,
                command=self.on_mode_selected)
        return self.__selector_widget

    @property
    def num_pad_widget(self):
        if not self.__num_pad_widget:
            options = range(1, len(self.items) + 1)
            self.__num_pad_widget = Tkinter.OptionMenu(
                self, Tkinter.IntVar(value=self.default_num), *options, command=self.on_num_selected)
            self.num = self.default_num
        return self.__num_pad_widget

    @property
    def item_list_widget(self):
        if not self.__item_list_widget:
            self.__item_list_widget = Tkinter.Listbox(self, selectmode=Tkinter.MULTIPLE)
            for item in self.items:
                self.__item_list_widget.insert(Tkinter.END, item)
            self.selected_item = self.default_list
            for item in self.default_list:
                self.__item_list_widget.select_set(item)
            self.__item_list_widget.bind("<<ListboxSelect>>", self.on_item_list_selected)
        return self.__item_list_widget

    def show(self):
        self.pack(pady=10, side=Tkinter.TOP)
        self.label_widget.pack(pady=10, side=Tkinter.TOP)
        self.selector_widget.pack(padx=20, pady=10, side=Tkinter.LEFT)
        self.on_mode_selected(ListChooseFrame.OPTIONS[self.default_mode])

    def on_mode_selected(self, value):
        self.mode = ListChooseFrame.OPTIONS.index(value)

        next_second_widget = None
        if value == ListChooseFrame.OPTIONS[1]:
            next_second_widget = self.num_pad_widget
        elif value == ListChooseFrame.OPTIONS[2]:
            next_second_widget = self.item_list_widget
        if next_second_widget != self.__current_second_widget and self.__current_second_widget:
            self.__current_second_widget.pack_forget()

        self.__current_second_widget = next_second_widget
        if self.__current_second_widget:
            self.__current_second_widget.pack(padx=20, pady=10, side=Tkinter.RIGHT)

    def on_num_selected(self, value):
        self.num = value

    def on_item_list_selected(self, event):
        self.selected_item = self.item_list_widget.curselection()

    def get(self):
        ret = None
        if self.mode == 1:
            ret = self.num
        elif self.mode == 2:
            ret = [self.items[i] for i in self.selected_item]
        return ListChooseFrame.OPTIONS[self.mode].lower(), ret

    def is_num_mode(self):
        return self.mode == 1

    def is_list_mode(self):
        return self.mode == 2


class FillBlankFrame(Tkinter.Frame):
    def __init__(self, master, default=True):
        Tkinter.Frame.__init__(self, master)
        self.__fill_blank = None
        self.default = default

    @property
    def fill_blank(self):
        if not self.__fill_blank:
            fill_blank_var = Tkinter.BooleanVar(value=self.default)
            self.__fill_blank = Tkinter.Checkbutton(
                self, text="Fill the blanks", var=fill_blank_var, command=self.on_fill_blank_selected)
            self.__fill_blank.var = fill_blank_var
            self.is_fill_blank = self.default
        return self.__fill_blank

    def show(self):
        self.pack(pady=10, side=Tkinter.TOP)
        self.fill_blank.pack(side=Tkinter.LEFT)

    def on_fill_blank_selected(self):
        self.is_fill_blank = self.fill_blank.var.get()

    def get(self):
        return self.is_fill_blank


class BackFrame(Tkinter.Frame):
    def __init__(self, master, on_back):
        Tkinter.Frame.__init__(self, master)
        self.__back_button = None
        self.on_back = on_back

    @property
    def back_button(self):
        if not self.__back_button:
            self.__back_button = Tkinter.Button(self, text="Back", command=self.on_back)
        return self.__back_button

    def show(self):
        self.pack(pady=10, side=Tkinter.TOP)
        self.back_button.pack(side=Tkinter.LEFT)


class ConfigFrame(Tkinter.Frame):
    def __init__(self, master):
        Tkinter.Frame.__init__(self, master)
        self.__mood_frame = None
        self.__tense_frame = None
        self.__fill_blank_frame = None
        self.__back_frame = None
        self.config = ExamConfig.create()

        self.sub_init = False

    def get_existed_config(self, type, type_num, type_list):
        if type in self.config:
            mode = self.config[type]
        else:
            mode = 1
        if type_num in self.config:
            num = self.config[type_num]
        else:
            num = 3
        if type_list in self.config:
            items = self.config[type_list]
        else:
            items = []
        return mode, num, items

    @property
    def mood_frame(self):
        if not self.__mood_frame:
            self.__mood_frame = ListChooseFrame(self, "Mood",
                                                ExamConfig.moods(), *self.get_existed_config(*ExamConfig.MOOD_KEY_WORD))
        return self.__mood_frame

    @property
    def tense_frame(self):
        if not self.__tense_frame:
            self.__tense_frame = ListChooseFrame(
                self, "Tense", ExamConfig.tenses(), *self.get_existed_config(*ExamConfig.TENSE_KEY_WORD))
        return self.__tense_frame

    @property
    def fill_blank_frame(self):
        if not self.__fill_blank_frame:
            self.__fill_blank_frame = FillBlankFrame(self, self.config[ExamConfig.FILL_BLANK])
        return self.__fill_blank_frame

    @property
    def back_frame(self):
        if not self.__back_frame:
            self.__back_frame = BackFrame(self, self.save)
        return self.__back_frame

    def show(self):
        self.place(relx=.1, rely=.1, anchor="nw")
        if self.sub_init:
            return
        self.mood_frame.show()
        self.tense_frame.show()
        self.fill_blank_frame.show()
        self.back_frame.show()
        self.sub_init = True

    def save_for_list(self, (type, type_num, type_list), frame):
        new_config = frame.get()
        self.config[type] = new_config[0]
        if frame.is_num_mode():
            self.config[type_num] = new_config[1]
        elif frame.is_list_mode():
            self.config[type_list] = new_config[1]

    def save_for_boolean(self, type, frame):
        self.config[type] = frame.get()

    @runtime
    def save(self):
        self.save_for_list(ExamConfig.MOOD_KEY_WORD, self.mood_frame)
        self.save_for_list(ExamConfig.TENSE_KEY_WORD, self.tense_frame)
        self.save_for_boolean(ExamConfig.FILL_BLANK, self.fill_blank_frame)
        self.config.dump_config()
        self.place_forget()
        self.master.window.switch_to_index()
