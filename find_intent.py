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


def match(sentence, pattern, thresh=0.5, debug=False):
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
            similarity = word_similarity(pattern_word[0], word[0]);
            if debug:
                print similarity
            if word[1] in pattern_word[1] and similarity < thresh:
                cursor = idx+1;
                matches.append(word)
                if debug:
                    print 'matched\n'
                break;
            else:
                if debug:
                    print 'no match'
    if (len(matches) == len(pattern)):
        return (True, matches)
    else:
        return (False, ())



pattern = [("launch", ("VB", "JJ", "NNP")), ("session",("NN",)), ("monday",("NNP","NN",))]

variations = [
    "Load my setup from yesterday.",
    "Open up the session from Tuesday.",
    "Open up the session from the bar.",
    "Open up session from November.",
    "Open session from November.",
    "Get the session from tomorrow",
    "Get the hamburger for tomorrow",
    "Launch monday's session"
]

for v in variations:
    print v
    print match(v, pattern, thresh=0.87, debug=True)
    print ''

pattern = [("switch", ("VB", "JJ", "NNP", "NN")), ("on",("IN","RP")), ("lights",("NNS","NN",))]

variations = [
    "Turn on the lights.",
    "Turn off the lights.",
    "Turn off the blender.",
    "Switch off the lights.",
    "Turn on the lamp.",
    "Toggle on the bulb.",
    "Toggle the bulb.",
    "Turn the light blue",
]

#for v in variations:
#    print v
#    print match(v, pattern, thresh=0.87)
#    print ''

