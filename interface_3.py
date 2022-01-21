# -*- coding: utf-8 -*-
"""
This file contains all the gui logic.
"""
import tkinter as tk
from tkinter import messagebox
from read_only_text_3 import ReadOnlyText
from seeker_3 import Seeker
from util_3 import clean, pyhash


FILE = 'files/sindarin_dictionary.db'
ICON = 'images/Celtic-Tree-of-Life-Symbol.png'
HELP = 'files/help.txt'
PASSWORD = '3cb778c938144f884d57f174abcccb34f250156f'
SINDARIN = 'Sin-Eng'
ENGLISH = 'Eng-Sin'
FONT_COLOR1 = 'black'
FONT_COLOR2 = 'blue'


class Caller:
    """
    This Class is a mean to replace the permanent lambda *args, **kwargs: ...
    constructions. It takes a function or method with its parameters and calls
    it, no matter the input.
    """
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return self.func(*self.args, **self.kwargs)


class AutoResizeText(ReadOnlyText):
    """
    This text widget resizes its rows to fit its contents. It is not meant
    to be writable.
    """
    def __init__(self, *args, **kwargs):
        super(AutoResizeText, self).__init__(*args, **kwargs)
        self.max_size = 3
        self.bind('<Configure>', self.auto_resize)
        self.bind('<<TextModified>>', self.auto_resize)

    def auto_resize(self, event):
        height = self.count_displayed("1.0", "end", "displaylines")
        if height <= self.max_size:
            self.config(height=height)

    def count_displayed(self, index1, index2, *args):
        args = [self._w, "count"] + ["-" + arg for arg in args] + [index1, index2]
        result = self.tk.call(*args)
        return result


class DefaultEntry(tk.Entry):
    """
    This class adds a default entry option.
    """
    def __init__(self, parent, default_text, *args, **kwargs):
        super(DefaultEntry, self).__init__(parent, *args, **kwargs)
        self.default_text = default_text
        self.default_fg = 'grey'
        self.normal_fg = 'black'
        self.default = False
        self.bind("<FocusIn>", lambda e: self._check(1))
        self.bind("<FocusOut>", lambda e: self._check(0))
        self._check(0)

    #TODO: Resolve cross-dependency between _default and _check
    def _default(self, exists):
        """
        Sublogic for displaying/hidding the default text.
        """
        self.default = exists
        if exists:
            self.insert(0, self.default_text)
            self.normal_fg = self.cget('fg')
            self.config(fg=self.default_fg)
        else:
            self.config(fg=self.normal_fg)

    def _check(self, mode):
        """
        Sets whether the default text should be displayed or not.
        """
        if mode:
            if self.default:
                self.delete(0, "end")
                self._default(False)
        else:
            if self.get() == '':
                self.delete(0, "end")
                self._default(True)

    def set_default(self, text):
        """
        Set the default text that will be shown if nothing is inserted.
        """
        self.default_text = text

    def get(self):
        """
        Return the text that is inserted, returns '' if nothing is inserted.
        """
        if self.default:
            return ''
        else:
            return self.tk.call(self._w, 'get')


class EditWindow:
    """
    """
    toplevel = None

    def __init__(self, parent):
        """
        """
        if self.toplevel is not None:
            self.toplevel.destroy()
        EditWindow.toplevel = tk.Toplevel(parent)

        self.toplevel.protocol('WM_DELETE_WINDOW', self.exit)
        self.edit_frame = tk.Frame(self.toplevel)
        self.word_entry = tk.Entry(self.edit_frame)
        self.meaning_entry = tk.Entry(self.edit_frame)
        self.tag_entry = tk.Entry(self.edit_frame)
        self.meaning_list = tk.Listbox(self.toplevel)
        self.scrollbar = tk.Scrollbar(self.toplevel, command=self.meaning_list.yview)
        self.meaning_list.config(yscrollcommand=self.scrollbar.set)
        self.button_frame = tk.Frame(self.toplevel)
        self.add_button = tk.Button(self.button_frame, text='Add', command=self.add)
        self.confirm_button = tk.Button(self.button_frame, text='Confirm', command=self.confirm)
        self.cancel_button = tk.Button(self.button_frame, text='Cancel', command=self.exit)

        self._setup()

    def _setup(self):
        """
        """
        self.toplevel.grid_rowconfigure(1, weight=1)
        self.toplevel.grid_columnconfigure(1, weight=1)
        self.edit_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        for i in range(2):
            self.edit_frame.grid_columnconfigure(i, weight=1, uniform='x-btn1')
        self.word_entry.grid(row=0, column=0, sticky='nsew')
        self.meaning_entry.grid(row=0, column=1, sticky='nsew')
        self.tag_entry.grid(row=1, column=0, columnspan=2, sticky='nsew')
        self.scrollbar.grid(row=1, column=0, sticky='nsew')
        self.meaning_list.grid(row=1, column=1, columnspan=2, sticky='nsew')
        self.button_frame.grid(row=2, column=0, columnspan=3, sticky='nsew')
        for i in range(3):
            self.button_frame.grid_columnconfigure(i, weight=1, uniform='x-btn2')
        self.cancel_button.grid(row=0, column=0, sticky='nsew')
        self.add_button.grid(row=0, column=1, sticky='nsew')
        self.confirm_button.grid(row=0, column=2, sticky='nsew')

    def exit(self, *args):
        """
        """
        self.toplevel.destroy()
        self.toplevel = None

    def add(self):
        """
        """
        pass

    def confirm(self):
        """
        """
        self.exit()


class HelpWindow:
    """
    """
    toplevel = None

    def __init__(self, parent):
        """
        """
        if self.toplevel is not None:
            self.toplevel.destroy()
        HelpWindow.toplevel = tk.Toplevel(parent)
        self.toplevel.protocol('WM_DELETE_WINDOW', self.exit)
        self.toplevel.minsize(400, 400)
        self.toplevel.title('Help Window')

        self.ranges = []
        self.max_var = tk.StringVar()
        self.max_var.set('0 \\')
        self.length_var = tk.IntVar()
        self.search_var = tk.StringVar()
        self.count = tk.IntVar()
        self.count.set(0)

        self.box = tk.Frame(self.toplevel)
        self.entry = tk.Entry(self.box, textvar=self.search_var)
        self.spin = tk.Spinbox(self.box, textvar=self.count, from_=0, to=0, increment=1,
                               command=self.see, state='readonly', width=5, wrap=True,
                               justify='left', relief='flat')
        self.max = tk.Label(self.box, textvar=self.max_var, width=5, anchor='e', relief='flat')
        self.button = tk.Button(self.box, text='Search', command=self.search)
        self.text = ReadOnlyText(self.toplevel, wrap='word')
        self.scroll = tk.Scrollbar(self.toplevel, command=self.text.yview)
        self.text.config(yscrollcommand=self.scroll.set)
        with open(HELP, 'r') as f:
            d = f.read()
        self.text.insert("1.0", d)
        self.entry.bind('<Return>', lambda e: self.search())

        self._setup()

    def _setup(self):
        """
        """
        self.toplevel.grid_columnconfigure(1, weight=1)
        self.toplevel.grid_rowconfigure(1, weight=1)
        self.box.grid_columnconfigure(0, weight=1)
        self.box.grid(row=0, column=0, columnspan=3, sticky='nsew')
        self.entry.grid(row=0, column=0, sticky='nsew')
        self.button.grid(row=0, column=1, sticky='nsew')
        self.spin.grid(row=0, column=3, sticky='nsew')
        self.max.grid(row=0, column=2, sticky='nsew')
        self.scroll.grid(row=1, column=0, sticky='nsew')
        self.text.grid(row=1, column=1, columnspan=3, sticky='nsew')

    def exit(self, *args):
        """
        """
        self.toplevel.destroy()
        self.toplevel = None

    def search(self):
        """
        """
        word = self.search_var.get()
        tag = "see"
        self.length_var.set(len(word))
        self.text.tag_remove(tag, "1.0", "end")
        self.text.tag_remove("high", "1.0", "end")
        if word == '':
            self.count.set(0)
            self.spin.config(from_=0, to=0)
            self.max_var.set("0 \\")
            self.ranges = []
            return
        start = '1.0'
        while True:
            start = self.text.search(word, start, tk.END)
            if start != '' and word != '':
                end = self.text.index('%s+%dc' % (start, (self.length_var.get())))
                self.text.tag_add(tag, start, end)
                self.text.tag_config(tag, background='yellow')
                start = end
            else:
                break
        self.ranges = self.text.tag_ranges("see")
        self.ranges = [i for idx, i in enumerate(self.ranges) if idx % 2 == 0]
        self.max_var.set(str(len(self.ranges)) + ' \\')
        if len(self.ranges) == 0:
            self.count.set(0)
            self.spin.config(from_=0, to=0)
        else:
            self.count.set(1)
            self.spin.config(from_=1, to=len(self.ranges))
        self.see()

    def see(self):
        """
        """
        self.text.tag_config("high", background="#ff6600")
        self.text.tag_remove("high", "1.0", "end")
        try:
            idx = self.count.get() - 1
            index = self.ranges[idx]
            self.text.tag_add("high", index, str(index) + ' + ' + str(self.length_var.get()) + ' chars')
            self.text.see(index)
        except IndexError:
            pass


class PasswordWindow:
    """
    The window where the user can enter the password to enter development mode.
    """
    toplevel = None

    def __init__(self, parent, var):
        """
        """
        if self.toplevel is not None:
            self.toplevel.destroy()
        PasswordWindow.toplevel = tk.Toplevel(parent)
        self.var = var
        self.entry = tk.Entry(self.toplevel, width=30, show='*')
        self.entry.bind('<Return>', lambda e: self.confirm())
        self.cancel_btn = tk.Button(self.toplevel, text='Cancel', command=self.exit)
        self.confirm_btn = tk.Button(self.toplevel, text='Confirm', command=self.confirm)

        self._setup()

    def _setup(self):
        """
        """
        self.toplevel.title('Password')

        for i in range(2):
            self.toplevel.grid_columnconfigure(i, weight=1, uniform='x-btn3')
        self.entry.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.cancel_btn.grid(row=1, column=0, sticky='nsew')
        self.confirm_btn.grid(row=1, column=1, sticky='nsew')

        self.entry.focus_set()

    def exit(self):
        """
        """
        self.toplevel.destroy()
        self.toplevel = None

    def confirm(self):
        """
        """
        if pyhash(self.entry.get(), 'sha1') == PASSWORD:
            self.var.set(True)
        else:
            self.var.set(False)
        self.exit()


class Interface:
    """
    The root window.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.seeker = Seeker()
        self.seeker.load(FILE)
        self.dictionary = None
        self.displayed = None

        self.development_mode = tk.BooleanVar()
        self.search_var = tk.StringVar()
        self.language_var = tk.StringVar()
        self.tag_var = tk.StringVar()
        self.type_var = tk.StringVar()
        self.specific_var = tk.BooleanVar()
        self.synonym_var = tk.BooleanVar()
        self.regex_var = tk.BooleanVar()
        self.language_options = {
            SINDARIN: self.seeker.get(),
            ENGLISH: self.seeker.get(True)
        }
        # Maybe there is a way to not hardcode these options?
        self.tag_options = [
            'All', 'Astron.', 'Cal.', 'Zool.', 'Biol.', 'Bot.', 'Orn.', 'Arch.', 'Poet.', 'Geog.', 'Geol.', 'Pop.'
        ]
        self.type_options = [
            'n.', 'v.', 'adv.', 'adj.', 'num.', 'pref.', 'pron.', 'ext.'
        ]
        self.tag_options.extend(self.type_options)  # remove when type options are implemented
        self.tag_options.sort()

        self.menu = tk.Menu(self.root, tearoff=0)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label='Open', command=self.not_implemented)
        self.file_menu.add_command(label='New', command=self.not_implemented)
        self.file_menu.add_command(label='Save', command=self.not_implemented)
        self.file_menu.add_command(label='Save As', command=self.not_implemented)
        self.edit_menu = tk.Menu(self.menu, tearoff=0)
        self.edit_menu.add_command(label='Undo', command=self.not_implemented)
        self.edit_menu.add_command(label='Redo', command=self.not_implemented)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label='Copy', command=self.not_implemented)
        self.edit_menu.add_command(label='Paste', command=self.not_implemented)
        self.edit_menu.add_command(label='Cut', command=self.not_implemented)
        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label='Help', command=self.create_help_window)
        self.help_menu.add_checkbutton(label='Developer Mode', onvalue=1, offvalue=0, var=self.development_mode,
                                       command=self.enable_developer_mode)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.menu.add_cascade(label='Edit', menu=self.edit_menu)
        self.menu.add_cascade(label='Help', menu=self.help_menu)

        self.frame = tk.Frame(self.root)
        self.view_box = tk.Frame(self.frame)
        self.word_entry = DefaultEntry(self.view_box, 'Search', width=20, textvar=self.search_var)
        self.word_entry.bind('<Return>', lambda e: self.search())
        self.word_entry.bind('<Key-Down>', lambda e: self.vocable_listbox.focus_set() or
                             self.vocable_listbox.selection_set(0))
        self.search_button = tk.Button(self.view_box, text='Search', command=self.search)
        self.option_box = tk.Frame(self.frame)
        self.language_chooser = tk.OptionMenu(self.option_box, self.language_var, *self.language_options.keys())
        self.language_chooser.config(width=8)
        self.tag_chooser = tk.OptionMenu(self.option_box, self.tag_var, *self.tag_options)
        self.tag_chooser.config(width=8)
        self.check_button3 = tk.Checkbutton(self.option_box, text='specific', var=self.specific_var, state='disabled')
        self.check_button2 = tk.Checkbutton(self.option_box, text='synonyms', var=self.synonym_var, state='disabled')
        self.check_button1 = tk.Checkbutton(self.option_box, text='regex', var=self.regex_var)
        self.vocable_listbox = tk.Listbox(self.frame)
        self.scrollbar = tk.Scrollbar(self.frame, command=self.vocable_listbox.yview)
        self.vocable_listbox.config(yscrollcommand=self.scrollbar.set, width=25)
        self.vocable_listbox.bind('<Double-1>', Caller(self.show))
        self.vocable_listbox.bind('<Return>', Caller(self.show))
        self.info_box = tk.Frame(self.frame)
        self.info_word1 = tk.Label(self.info_box, text='Word', width=10, anchor='ne', padx=2)
        self.vocab_entry1 = ReadOnlyText(self.info_box, width=20, height=1)
        self.info_word2 = tk.Label(self.info_box, text='Meanings', width=10, anchor='ne', padx=2)
        self.vocab_entry2 = AutoResizeText(self.info_box, width=20, height=1)
        self.description_text = ReadOnlyText(self.info_box, width=90)
        self.edit_button = tk.Button(self.info_box, text='Edit', command=self.create_edit_window)

        # self.search_var.trace('w', Caller(self.search))
        self.word_entry.bind('<KeyRelease>', Caller(self.search))
        self.language_var.trace('w', Caller(self.change_dictionary))
        self.language_var.set(SINDARIN)
        self.tag_var.trace('w', Caller(self.search))
        self.tag_var.set(self.tag_options[0])
        self.type_var.set(self.type_options[0])

        self.find('')
        self._setup()

    def _setup(self):
        self.root.geometry('578x435')
        self.root.minsize(300, 300)
        self.root.title('Seeker Interface')
        self.root.protocol('WM_DELETE_WINDOW', Caller(self.stop))
        self.root.config(menu=self.menu)
        self.root.iconphoto(False, tk.PhotoImage(file=ICON))
        # program.tk.call('wm','iconphoto', program._w,tk.PhotoImage(file=ICON))

        self.frame.pack(fill='both', expand=1, padx=5, pady=5)
        self.view_box.pack(side='top', fill='x', anchor='n')
        self.word_entry.pack(side='left', expand=1, fill='x')
        self.search_button.pack(side='left')
        self.option_box.pack(side='top', fill='x', anchor='n')
        self.language_chooser.pack(side='left')
        self.tag_chooser.pack(side='left')
        self.check_button1.pack(side='right')
        self.check_button2.pack(side='right')
        self.check_button3.pack(side='right')
        self.scrollbar.pack(side='left', fill='y')
        self.vocable_listbox.pack(side='left', fill='both', expand=1)
        self.info_box.pack(side='right', fill='both', expand=1)
        self.info_box.grid_rowconfigure(2, weight=1)
        self.info_box.grid_columnconfigure(1, weight=1)
        self.info_word1.grid(row=0, column=0, sticky='nsew')
        self.vocab_entry1.grid(row=0, column=1, sticky='nsew')
        self.info_word2.grid(row=1, column=0, sticky='nsew')
        self.vocab_entry2.grid(row=1, column=1, sticky='nsew')
        self.description_text.grid(row=2, column=0, columnspan=2, sticky='nsew')
        self.edit_button.grid(row=3, column=0, columnspan=2)

    def start(self):
        """
        Call to start the program.
        """
        self.root.mainloop()

    def stop(self, ask=True):
        """
        Call to end the program. When ask is set to False the program will
        terminate without promting for confirmation.
        """
        if ask:
            if messagebox.askyesno('Exit', 'Do you want to exit?'):
                self.root.destroy()
        else:
            self.root.destroy()

    def insert(self, ls, sort=True):
        """
        """
        if sort:
            ls = sorted(ls, key=clean)
        self.vocable_listbox.delete(0, "end")
        for idx, item in enumerate(ls):
            self.vocable_listbox.insert(idx, item)

    def change_dictionary(self):
        """
        """
        self.dictionary = self.language_options[self.language_var.get()]
        self.search()

    def highlight_word(self, tag, exists):
        """
        """
        if exists:
            self.vocab_entry2.tag_config(tag, foreground=FONT_COLOR2, relief='raised', underline=1)
            self.vocab_entry2.config(cursor='')
        else:
            self.vocab_entry2.tag_config(tag, foreground=FONT_COLOR1, relief='flat', underline=0)
            self.vocab_entry2.config(cursor='xterm')

    def find(self, word):
        """
        """
        word = word
        specific = self.specific_var.get()
        if specific:
            print(self.dictionary.get(word))
            return
        tag = self.tag_var.get()
        regex = self.regex_var.get()
        if tag == 'All':
            tag = None
        ls = self.dictionary.like(word, tag, regex)
        self.insert(ls)

    def search(self):
        """
        """
        self.find(self.search_var.get())

    def show(self):
        """
        """
        try:
            idx = self.vocable_listbox.curselection()[0]
            key = self.vocable_listbox.get(idx)
            word = self.dictionary.get(key)
            self.displayed = self.language_var.get()
            self.display(word)
        except IndexError:
            print('Nothing Selected')

    def display(self, word):
        """
        """
        try:
            self.vocab_entry1.delete("1.0", "end")
            self.vocab_entry2.delete("1.0", "end")
            self.vocab_entry1.insert("1.0", word.key)
            pi = [1, 0]
            for idx, meaning in enumerate(word.meanings):
                self.vocab_entry2.insert("end", meaning)
                tag = 'see_' + str(idx)
                self.vocab_entry2.tag_add(tag, f'{pi[0]}.{pi[1]}', "end - 1 chars")
                self.vocab_entry2.tag_config(tag, foreground=FONT_COLOR1, relief='flat', underline=0)
                self.vocab_entry2.tag_bind(tag, '<Button-1>', Caller(self.go_to, meaning))
                self.vocab_entry2.tag_bind(tag, '<Enter>', Caller(self.highlight_word, tag, True))
                self.vocab_entry2.tag_bind(tag, '<Leave>', Caller(self.highlight_word, tag, False))
                pi[1] += len(meaning)
                if idx < len(word.meanings)-1:
                    self.vocab_entry2.insert("end", ', ')
                    pi[1] += 2
            text = '[' + '+'.join(word.tags) + ']\n'
            self.description_text.delete("1.0", "end")
            self.description_text.insert("1.0", text)
            self.vocab_entry2.auto_resize(None)
        except Exception as e:
            print('could not load word.', e)

    def go_to(self, key):
        """
        """
        if self.displayed == SINDARIN:
            self.displayed = ENGLISH
        elif self.displayed == ENGLISH:
            self.displayed = SINDARIN
        word = self.language_options[self.displayed].get(key)
        self.display(word)

    def create_edit_window(self):
        """
        """
        if not self.development_mode.get():
            messagebox.showinfo('Access Denied', 'Developer mode is not enabled.')
            return
        EditWindow(self.root)

    def create_help_window(self):
        """
        """
        HelpWindow(self.root)

    def enable_developer_mode(self, *args):
        """
        """
        self.development_mode.set(False)
        PasswordWindow(self.root, self.development_mode)

    @staticmethod  # Remove if not needed anymore
    def not_implemented():
        """
        This message will be called if the user tries to access a feature
        that has not been implemented yet.
        """
        messagebox.showinfo('Info', 'Not Implemented')


if __name__ == '__main__':
    app = Interface()
    app.start()

# TODO: Export all Methods to classes
# TODO: Solve cross dependency between windows
# TODO: Add multiple language translation support
