import sys
import h5py
import hashlib
import numpy as np
import nltk
from scipy.spatial import distance
f = h5py.File("data/word_embeddint.hdf5", "r")


def word_to_vec(word):
    key = hashlib.md5(word.lower()).hexdigest()
    return f[key][:]
            
def word_similarity(word_a, word_b):
    vec_a = word_to_vec(word_a)
    vec_b = word_to_vec(word_b)
    return distance.cosine(vec_a, vec_b)


def match(sentence, pattern, thresh=0.6, debug=False):
    words = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(words)
    fragment = tagged
    cursor = 0
    matches = []
    for pattern_word in pattern:
        fragment = fragment[cursor:]
        for idx, word in enumerate(fragment):
            if debug:
                print pattern_word, word
            if word[1] in pattern_word[1] and word_similarity(pattern_word[0], word[0]) < thresh:
                cursor = idx+1;
                matches.append(word)
                if debug:
                    print 'matched'
                break;
            else:
                if debug:
                    print 'no match'
    if (len(matches) == len(pattern)):
        return (True, matches)
    else:
        return (False, ())



pattern = [("launch", ("VB",)), ("session",("NN",)), ("monday",("NNP","NN",))]

print match("Open up the session from Tuesday.", pattern)
print match("Open up session from November.", pattern)
print match("Open session from November.", pattern, debug=True)
print match("Get the session from tomorrow", pattern)
print match("Get the hamburger for tomorrow", pattern)
