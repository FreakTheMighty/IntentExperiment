from flask import Flask, jsonify, request
import requests
import h5py
import hashlib
from scipy.spatial import distance

app = Flask(__name__)
embedding_file = h5py.File("data/word_embeddint.hdf5", "r")

def word_to_vec(word):
    key = hashlib.md5(word.lower()).hexdigest()
    return embedding_file[key][:]
            
def word_similarity(word_a, word_b):
    vec_a = word_to_vec(word_a)
    vec_b = word_to_vec(word_b)
    return distance.cosine(vec_a, vec_b)

def semregex(content, pattern):
    params = {"pattern": pattern}
    r = requests.post('http://corenlp:9000/semgrex', data=content, params=params)
    return r.json()

class Intent(object):

    def __init__(self, grammars, group_names, vocabs, threshold=.75):
        self.grammars = grammars;
        self.group_names = group_names
        self.vocabs = vocabs
        self.threshold = threshold

    def match(self, content):
        found = None
        match = False
        result = {"match": False, "slots": {}}

        for g in self.grammars:
            matches = semregex(content, g)
            if matches["sentences"][0]["length"]:
                found = matches["sentences"][0]["0"]
                break;

        if found:
            for vocab in self.vocabs:
                similar = True
                for group_name, sample_word in zip(self.group_names, vocab):
                    vocab_match = found[group_name]["text"]
                    similarity = word_similarity(vocab_match, sample_word)
                    
                    print vocab_match, sample_word
                    print similarity
                    print "\n"
                    result["slots"][group_name] = vocab_match
                    if similarity > self.threshold:
                        similar = False
                    
                if similar:
                    result["match"] = True
                    break;
                else:
                    result["slots"] = {}

        return result;


            



@app.route('/')
def run():
    content = request.args.get('content')
    grammars = [
        "{pos:/VB.*/}=command  >dobj {}=object  > /nmod:.*/ {}=time",
        "{pos:/VB.*/}=command  >dobj ({}=object  > /nmod:.*/ {}=time)"
    ]
    vocabs = [["launch", "session", "monday"]]
    intent = Intent(grammars, ["$command","$object", "$time"], vocabs)
    return jsonify(intent.match(content))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

