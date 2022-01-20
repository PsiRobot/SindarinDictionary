import os
import json
import sqlite3 as sql
from dictionary_3 import Dictionary


DICTIONARY = 'dictionary'
FILE = 'files/sindarin_dictionary.db'


class Seeker:
    def __init__(self):
        self.dictionary = dict()

    def load(self, file, path=None):
        path = path if path is not None else os.path.dirname(__file__)
        file = os.path.join(path, file)
        self._dbinit(file)
        self.dictionary = self._extract(file)

    @staticmethod
    def _table_list(file):
        with sql.connect(file) as con:
            cur = con.cursor()
            res = cur.execute("""
                SELECT name FROM sqlite_master WHERE type='table';
                """)
        return res.fetchall()

    @staticmethod
    def _dbinit(file):
        with sql.connect(file) as con:
            cur = con.cursor()
            cmd = f"""
                CREATE TABLE IF NOT EXISTS {DICTIONARY}(id INTEGER PRIMARY KEY,
                sd TEXT, en TEXT, tag TEXT, ls TEXT);
                """
            cur.execute(cmd)
            con.commit()

    @staticmethod
    def _extract(file):
        with sql.connect(file) as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cmd = f"""
                SELECT id, sd, en, tag, ls FROM {DICTIONARY};
                """
            res = cur.execute(cmd)
            res = {i[0]: i[1:] for i in res.fetchall()}
        return res

    @staticmethod
    def _insert(cur, idx, sid, eng, tag, ls):
        cmd = f"""
            INSERT INTO {DICTIONARY} (id, sd, en, tag, ls) VALUES (?, ?, ?, ?, ?)
            """
        cur.execute(cmd, (idx, sid, eng, tag, ls))

    @staticmethod
    def backup(dictionary, file):
        with open(file, 'w') as f:
            txt = json.dumps(dictionary)
            f.write(txt)

    def _write(self, file):
        try:
            with sql.connect(file) as con:
                cur = con.cursor()
                cur.execute(f'DROP TABLE {DICTIONARY}')
                self._dbinit(file)
                for idx, word in enumerate(self.dictionary.values()):
                    sid, eng, tag, ls = word
                    self._insert(cur, idx, sid, eng, tag, ls)
                con.commit()
        except Exception as e:
            print(e)
            print('Please Backup the dictionary before closing')
            self.backup(self.dictionary, 'backup.txt')

    def get(self, reverse=False):
        dictionary = Dictionary()
        if not reverse:
            for value in self.dictionary.values():
                word, meaning, tag, _ = value
                tag = tag.split('+')
                dictionary.add(word, meaning, tag)
        else:
            for value in self.dictionary.values():
                word, meaning, tag, _ = value
                tag = tag.split('+')
                dictionary.add(meaning, word, tag)
        return dictionary

    def update(self, dictionary: Dictionary):
        # Make sure to not update with the reversed dictionary!
        if not isinstance(dictionary, Dictionary):
            raise TypeError(dictionary)
        new_dict = dict()
        idx = 0
        for word in dictionary.values():
            for meaning, tags in zip(word.words.keys(), word.words.values()):
                new_dict[idx] = [word.key, meaning, '+'.join(tags), word.ls]
                idx += 1
        self.dictionary = new_dict


if __name__ == '__main__':
    view = Seeker()
    view.load(FILE)
    sd = view.get()
    en = view.get(True)

    enstr = ""
    for word in en.values():
        enstr += word.key + ";" + ", ".join(word.meanings) + "\n"


    destr = ""
    for word in sd.values():
        destr += word.key + ";" + ", ".join(word.meanings) + "\n"
