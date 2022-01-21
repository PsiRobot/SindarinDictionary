# -*- coding: utf-8 -*-
from word_3 import Word
from util_3 import like, match


class Dictionary:
    """
    This class represents a collection of words and meanings.
    The key is string and the value a "Word" object.
    """
    def __init__(self):
        self.data = dict()

    def keys(self, tag=None):
        """
        Return the dictionaries keys.
        """
        if tag is None:
            return list(self.data.keys())
        else:
            return [i.key for i in self.data.values() if tag in i.tags]

    def values(self, tag=None):
        """
        Return the dictionaries values.
        """
        if tag is None:
            return [i for i in self.data.values()]
        else:
            return [i for i in self.data.values() if tag in i.tags]

    def items(self):
        """
        Return items as tuple(key, value).
        """
        return self.data.items()

    def get(self, word):
        """
        Return meanings linked to word.
        """
        return self.data.get(word)

    def add(self, word, meaning, tag):
        """
        Add a new entry.
        """
        if word in self.data:
            self.data[word].update(meaning, tag)
        else:
            self.data[word] = Word(word, meaning, tag)

    def set(self, word, meaning: Word):
        """
        Set existing meanings.
        """
        if not isinstance(meaning, Word):
            raise TypeError(meaning)
        if word in self.data:
            self.data[word] = meaning
        else:
            self.data[word] = meaning

    def like(self, word, tag=None, regex=False):
        """
        Returns a list of all words that match "word". If regex is set to True
        "word" will be treated as regex-string. If tag is set only words
        that have the tag will be in the list.
        """
        ls = self.keys(tag)
        if not regex:
            return [key for key in ls if like(word, key)]
        else:
            return [key for key in ls if match(word, key)]

    def sort(self):
        """
        Sort the dictionary.
        """
        self.data = {key: word for key, word in sorted(self.data.items(), key=lambda x: x[0])}


if __name__ == '__main__':
    d = Dictionary()
