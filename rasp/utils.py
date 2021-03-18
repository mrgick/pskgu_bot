# Различные утилиты.

import re

def word_diff(word1, word2, minmatch):
    i = 0
    j = 0
    word1_len = len(word1)
    word2_len = len(word2)
    n = min(word1_len, word2_len)
    minmatch = min(minmatch, max(word1_len, word2_len))
    m = 0
    while i < n:
        if word1[i] == word2[j]:
            m += 1
            j += 1
        else:
            j = 0
        if m >= minmatch:
            return True
        i += 1

def test_by_words(query, name, minmatch):
    query = query.lower()
    name = name.lower()
    query_words = re.findall(r"([^\s()]+)", query)
    name_words = re.findall(r"([^\s()]+)", name)
    i = 0
    n = len(name_words)
    query_n = len(query_words)
    while i < n:
        j = 0
        end = n - i
        while j < end  and j < query_n:
            if word_diff(query_words[j], name_words[i + j], minmatch=minmatch):
                return True
            j += 1
        i += 1
    return False

