# Filter Words

This was a code challenge that is closer to a FizzBuzz style test, including more
oppertunities to ask clarifying questions to keep it simple. The main stated goal was
to work through it together and articulate thoughts and strategy. The technical goal is to see
that a list of words can be filtered against a known dictionary along with a few other
constraints.

Clarifying that formatting doesn't matter makes this problem simple. A regex is a very
fast way to do the word checking, albeit looping through characters and checking for `a-z`
is a more explicit way, if exact performance is desired. An key observation for optimization
is noticing that the dictionary itself contains invalid words that could be filtered upfront.

---

We want to check whether a string of words are valid words or not.

A word is valid if it is:

* found in our dictionary; named `DICTIONARY` in the code sample
* not a proper noun
* purely alphabetic; meaning no numbers or other symbols

The input string can contain any number of words separated by spaces.

Output whether each word is valid or not on individual lines.

For example, the input "dog Casey nostalgia 3M" should output:

```
dog is a word
Casey is not a word
nostalgia is a word
3M is not a word  
```

See the full list in [`words.txt`](./words.txt) (originally from [dwly/english-words](https://github.com/dwyl/english-words/)). 
Below are some example words.

```
AARC
aardvark
aardvarks
aardwolf
aardwolves
Aaren
Aargau
```

## Solution

This ends up not being a tricky problem. It is more about reading the requirements, 
looking at example data and doing the minimal appropriate amount of work. A few key
things were noticed about this problem.

1. Constraints for valid words end up meaning only lowercase letters (regex `[a-z]*`)
2. The list of words itself contains many invalid words. Don't match against these.
3. Making a set from the valid dictionary words is helpful so that later checks against
   it can be fast `O(1)` vs reiterating the entire list.

Below is the example code from [`filter_words.py`](./filter_words.py).

```
import requests
import re


r = requests.get("https://raw.githubusercontent.com/dwyl/english-words/master/words.txt")

# valid to assume one word per line and no extra whitespaces
DICTIONARY = r.text.splitlines()

# NDFA -> DFA conversion can be expensive (not really here) do it once
valid_word_regex = re.compile(r'[a-z]*')

# O(1) check of any word to the set of valid words
def valid_word(word):
  # make sure all lowercase alphabetic
  return valid_word_regex.fullmatch(word)

# set of the valid words from the dictionary, which means all lowercase alphabetic characters
valid_words = {w for w in DICTIONARY if valid_word(w)}

# O(N) tests each unique word against the list
def check_words(words_to_check):

  # valid to assume input is always seperated by exaxtly one space (aka ' ')
  words = {w for w in words_to_check.split(' ')}

  # check each word from the split line; N words each with O(1) lookup means O(N) complexity
  for word in words:
    if valid_word(word) and word in valid_words:
      print(f'{word} is a word')
    else:
      print(f'{word} is not a word')


sample_input = "dog Casey nostalgia 3M"
print(f"Checking words: '{sample_input}'")
check_words(sample_input)
```

Output from the above matches the example, as expected. It also matches in an bonus,
edge case where repeats appear in the line. e.g. `dog Casey nostalgia 3M nostalgia`
