# -*- coding: utf-8 -*-
class Word:
    """
    The "Word" class is used for storing the connection between words of
    different languages.
    """
    def __init__(self, key: str, meaning: str, tags: list):
        self.key      = key
        self.words    = {meaning: tags.copy()}
        self.meanings = [meaning]
        self.tags     = tags
        self.ls       = None

    def __str__(self):
        return f"{self.key}: [{'+'.join(self.tags)}] {', '.join(self.meanings)}"

    def update(self, meaning, tags):
        """
        Add meaning and tags
        """
        self.words[meaning] = tags
        self.meanings.append(meaning)
        for tag in tags:
            if tag not in self.tags:
                self.tags.append(tag)
