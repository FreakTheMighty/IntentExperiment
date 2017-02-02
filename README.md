# Intent Experiment


## To run


```bash
$ docker-compose up
$ curl -G "http://192.168.99.100:5000" --data-urlencode "content=Open the session from Tuesday"
```

Responds:

```json
{
  "match": true, 
  "slots": {
    "$command": "Open", 
    "$object": "session", 
    "$time": "Tuesday"
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

The intent is defined as a list of grammar rules and a list of sample slot words.
A chunk of text is a match, if it matches any of the grammar rules, and the candidate
slots are similar enough to the example words. "Similar enough" is defined as a fixed
threshold for the cosine distance between the two words.

```python

grammars = [
    "{pos:/VB.*/}=command  >dobj {}=object  > /nmod:.*/ {}=time",
    "{pos:/VB.*/}=command  >dobj ({}=object  > /nmod:.*/ {}=time)"
]

vocabs = [
    ["launch", "session", "monday"],
    ["open", "session", "september"]
]

intent = Intent(grammars, ["$command", "$object", "$time"], vocabs)
```

We the run the intent like so:

```python
print(intent.match("Launch the session for yesterday"))

{
  "match": true, 
  "slots": {
    "$command": "Launch", 
    "$object": "session", 
    "$time": "yesterday"
  }
}
```




