import re
import hashlib

rep = {
    'î': 'i', 'í': 'i', 'û': 'u', 'ú': 'u', 'ó': 'o', 'ë': 'e', 'é': 'e',
    'â': 'a', 'ŷ': 'y', 'ý': 'y', 'ö': 'oe', 'ü': 'ue', 'ä': 'ae', '(': '',
    ')': '', '[': '', ']': '', '?': '', "'": '', '"': ''
}

hash_algorithms = {
    'sha1': hashlib.sha1, 'md5': hashlib.md5,
    'sha224': hashlib.sha224, 'sha256': hashlib.sha256,
    'sha384': hashlib.sha384, 'sha512': hashlib.sha512,
    'blake2b': hashlib.blake2b, 'blake2s': hashlib.blake2s,
    'sha3_224': hashlib.sha3_224, 'sha3_256': hashlib.sha3_256,
    'sha3_384': hashlib.sha3_384, 'sha3_512': hashlib.sha3_512
    }


def pyhash(string, alg):
    """
    return the hash from hash algorythmus alg
    >>> pyhash('Hello World', 'sha1')
    '0a4d55a8d778e5022fab701977c5d840bbc486d0'
    """
    hsh_alg = hash_algorithms[alg]
    wrd = string.encode('utf-8')
    wrd = wrd.strip()
    wrd_hsh = hsh_alg(wrd)
    wrd_hsh = wrd_hsh.hexdigest()
    return wrd_hsh.strip()


def clean(string):
    string = string.lower()
    chars = {'"': '', "'": '', '(': '', ')': '', '?': ''}
    for k, v in zip(chars.keys(), chars.values()):
        string = string.replace(k, v)
    string = string.strip()
    return string


def like(x, y):
    x, y = x.lower().strip(), y.lower().strip()
    for k, v in zip(rep.keys(), rep.values()):
        x = x.replace(k, v)
        y = y.replace(k, v)
    if y.find(x) != -1:
        return True


def match(regex, word):
    try:
        if re.match(regex, word) is not None:
            return True
        else:
            return False
    except re.error:
        return False


if __name__ == '__main__':
    from doctest import testmod
    testmod()
