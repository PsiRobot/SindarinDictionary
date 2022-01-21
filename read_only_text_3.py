# -*- coding: utf-8 -*-
from tkinter import Text

commands_to_remove = (
    "<Control-Key-h>",
    "<Meta-Key-Delete>",
    "<Meta-Key-BackSpace>",
    "<Meta-Key-d>",
    "<Meta-Key-b>",
    "<<Redo>>",
    "<<Undo>>",
    "<Control-Key-t>",
    "<Control-Key-o>",
    "<Control-Key-k>",
    "<Control-Key-d>",
    "<Key>",
    "<Key-Insert>",
    "<<PasteSelection>>",
    "<<Clear>>",
    "<<Paste>>",
    "<<Cut>>",
    "<Key-BackSpace>",
    "<Key-Delete>",
    "<Key-Return>",
    "<Control-Key-i>",
    "<Key-Tab>",
    "<Shift-Key-Tab>"
)


class ReadOnlyText(Text):
    """
    A text widget that can not be used for writing by removing all bindings
    assoziated with writing text. This unbinding happens on class level.
    """
    tag_init = False

    def __init__(self, *args, **kw):
        Text.__init__(self, *args, **kw)
        if not ReadOnlyText.tag_init:
            self.init_tag()
        bind_tags = (tag if tag != "Text" else "ReadOnlyText" for tag in self.bindtags())
        self.bindtags(bind_tags)

    # Unbindings as argument?
    def init_tag(self):
        """
        Removes all specified options
        """
        for key in self.bind_class("Text"):
            if key not in commands_to_remove:
                command = self.bind_class("Text", key)
                self.bind_class("ReadOnlyText", key, command)
        ReadOnlyText.tag_init = True
