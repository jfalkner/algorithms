"""
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
"""
import requests
import re


r = requests.get("https://raw.githubusercontent.com/dwyl/english-words/master/words.txt")
# assume single word per line
DICTIONARY = r.text.splitlines()

valid_word_regex = re.compile(r'[a-z]*')


# O(1)
def valid_word(word):
    # make sure all lowercase alphabetic
    return valid_word_regex.fullmatch(word)


# set of the valid words from the dictionary, which means all lowercase alphabetic characters
valid_words = {w for w in DICTIONARY if valid_word(w)}


# O(N)
def check_words(words_to_check):

    # split the line by whitespace
    words = {w for w in words_to_check.split(' ')}

    # check each word from the split line
    for word in words:
        if valid_word(word) and word in valid_words:
            print(f'{word} is a word')
        else:
            print(f'{word} is not a word')


sample_input = "dog Casey nostalgia 3M nostalgia"
print(f"Checking words: '{sample_input}'")
check_words(sample_input)
