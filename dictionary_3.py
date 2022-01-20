from word_3 import Word
from util_3 import like, match


class Dictionary:
    def __init__(self):
        self.array = dict()

    def keys(self, tag=None):
        if tag is None:
            return list(self.array.keys())
        else:
            return [i.key for i in self.array.values() if tag in i.tags]

    def values(self, tag=None):
        if tag is None:
            return [i for i in self.array.values()]
        else:
            return [i for i in self.array.values() if tag in i.tags]

    def items(self):
        return self.array.items()

    def get(self, word):
        return self.array.get(word)

    def add(self, key, meaning, tag):
        if key in self.array:
            self.array[key].update(meaning, tag)
        else:
            self.array[key] = Word(key, meaning, tag)

    def set(self, key, word: Word):
        if not isinstance(word, Word):
            raise TypeError(word)
        if key in self.array:
            self.array[key] = word
        else:
            self.array[key] = word

    def like(self, word, tag=None, regex=False):
        ls = self.keys(tag)
        if not regex:
            return [key for key in ls if like(word, key)]
        else:
            return [key for key in ls if match(word, key)]

    def sort(self):
        self.array = {key: word for key, word in sorted(self.array.items(), key=lambda x: x[0])}


if __name__ == '__main__':
    d = Dictionary()
