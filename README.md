# Intent Experiment


## To run


```bash
$ docker-compose up
$ curl -G "http://192.168.99.100:5000" --data-urlencode "content=Grab the notes from yesterday"
```

Responds:

```json
{
  "match": true,
  "slots": {
    "$command": "Grab",
    "$object": "notes",
    "$time": "yesterday"
  }
}
```

## Overview

This is an experiment in identifying intent and slots. 
This combines a grammatical match with similarity comparison 
of sample words to determine weather and
test phrase matches an intent.

Note that at the moment this is hardcoded to test the supplied phrase
against a single hardcoded intent. The match in binary, the content is 
either a match or it isn't.

The intent is defined like so:

```python

grammars = [
    "{pos:/VB.*/}=command  >dobj {}=object  > /nmod:.*/ {}=time",
    "{pos:/VB.*/}=command  >dobj ({}=object  > /nmod:.*/ {}=time)"
]

vocabs = [
        ["launch", "session", "monday"],
        ["grab", "note", "monday"],
]
intent = Intent(grammars, ["$command", "$object", "$time"], vocabs)

```

The intent is defined as a list of grammar rules and a list of sample slot words.
A chunk of text is a match, if it matches any of the grammar rules, and the candidate
slots are similar enough to the example words. "Similar enough" is defined as a fixed
threshold for the cosine distance between the two words.
