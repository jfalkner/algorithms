# Trie for DNA Sequences

This is an example of using a [trie](https://en.wikipedia.org/wiki/Trie) for two
specific purposes: efficiently representing DNA sequences and having a method to take a
set of characters and estimate the fraction of letters in the list of strings used to
build the trie from the target data set. An alphabet of (A, C, T, G, N) will be used.

For example, if the list of strings used to construct the trie is {ACTG, AACT, TCAGG,
TTGGA} and the set of target characters is {G, C} then the result is roughly 0.44 (8/18).

Trie's have a lookup time dependent on the length of the word but not the number of
strings used to build the trie (aka prefix tree). e.g. `O(n)` where `n` is the length
of the word. Keeping this `O(n)` magnitude performance is desired here but more focus
is on efficient memory usage considering two things:

1. Python can be inefficient. A language constraint. e.g. `dict` is relatively easy to
   use but uses relatively lots of memory, objects use an internal `dict` by default
   for properties and other optimizations such as `__slots__` and dataclasses exist for
   a reason.
2. DNA sequences can often have many similar repeating elements. A domain-specific
   observation. 

Below summarizes minimal work to pick out a relatively memory efficient trie
representation and later refinement to try and optimize for repetitive DNA sequences.
[Python's functional style of coding](https://docs.python.org/3/howto/functional.html) is used to keep data and functions concise and pure,
easily testable (by the doctest module in this case).

## Estimating Memory Efficiency

Below considers memory options for the first issue: Python. It assumes a more classic
trie with a node for every possible character in the alphabet. This approximates worst
size since no other optimizations are done. A per node counter is kept noting how many
words ended at that node. e.g. 6 vars per node: references to child nodes for A, C, G, T, N and an int `count`. 

Here are valid ways this could be represented.

* `class` with instance variables referencing subsequent nodes in the trie
* `class` with `__slots__` to avoid normal object `dict` overhead
* `dict` with each letter being a key pointing to subsequent `dict` instances for the trie.
* `namedtuple` with similar fields as the dict
* `tuple` with fixed positions for each letter and otherwise replacing the dict

[`pympler`](https://pympler.readthedocs.io/en/latest/) is used to get how much memory
Python objects use.


See the [`memory_usage.py`](./memory_usage.py) Python script that makes up an example of each above and
produces the below results. It was run using a `venv` and the `requirements.txt`
dependencies from this folder.

```
# using 3.9.6
python -V
Python 3.9.6

# install all dependencies
python3.9 -m venv .VENV
source .VENV/bin/activate
python -m pip install -r requirements.txt

# run the above script
python memory_usage.py


Memory Usage Per Datastructure

* Class = 448
* Class w/__slots__ = 120
* Dict = 736
* namedtuple = 128
* Tuple = 128
```

It appears that a Python class with `__slots__` will work well, which is nice since it
allows intuitive naming of instance variables A, C, T, G, and N versus indexes in a
tuple.

### Algorithm and Results

The algorithm was implemented in two parts:

* [`trie_dna.py`](trie_dna.py) succinct and minimally memory optimized via `__slots__` to avoid Python `dict` overhead
* [`trie_dna_optimized.py`](trie_dna_optimized.py) optimized data structure representation and domain-specific optimization for repetitive sequences. Same code as `trie_dna.py` but extended to make the trie use substantially less memory.


Before showing the code, notice that Python's `doctest` module was used to in-line
test examples and edge cases directly in the code. Run them to see that they pass.


```
# run the tests in this modules method comments
python -m doctest -v trie_dna_optimized.py


Trying:
    calculate_fraction(make_trie([]), {'A'})
Expecting:
    Traceback (most recent call last):
     ...
    ValueError: Can not estimate frequency if no sequences are provided
ok
Trying:
    calculate_fraction(make_trie(['A', 'C', 'T', 'G']), {'A'})
Expecting:
    0.25
ok
Trying:
    calculate_fraction(make_trie(['ACTG', 'AACT', 'TCAGG', 'TTGGA']), {'G', 'C'})
Expecting:
    0.4444444444444444
ok
Trying:
    calculate_fraction(make_trie(['ACTG', 'AACT', 'TCAGG', 'TTGGA']), {'A', 'C', 'G', 'T'})
Expecting:
    1.0
ok
Trying:
    calculate_fraction(make_trie(['ACTG', 'AACT', 'TCAGG', 'ACTG', 'ACTG', 'GGCG', 'TTGGA']), {'C', 'G'})
Expecting:
    0.5333333333333333
ok
Trying:
    calculate_fraction(make_trie(['CGGCGGA', 'CGGCGGC', 'CGGCGGG', 'CGGCGGT', 'CGGCGGN']), {'C', 'G'})
Expecting:
    0.9142857142857143
ok
1 items passed all tests:
   6 tests in trie_dna_optimized.calculate_fraction
6 tests in 15 items.
6 passed and 0 failed.
Test passed.
```

See [`trie_dna.py`](trie_dna.py) for a succinct version of a trie using a Python class with
`__slots__`, which saves on the overhead of normal Python object creation (see [`memory_usage.py`](memory_usage.py)), including
preventing the per-object `dict`. This code is ~100 lines and solves the main challenge.

[`trie_dna_optimized.py`](trie_dna_optimized.py) is discussed more below. It is more interesting because it uses
both Python memory optimization and algorithm implementation-specific memory
optimization. A simliar memory test was done using [`memory_usage_optimized.py`](memory_usage_optimized.py) and has
the output shown below.

```
python memory_usage_optimized.py

Memory Usage Per Data Structure

* Unoptimized (trie_dna.py) = 1784
* Optimized (trie_dna_optimized.py) = 1232
* Optimized Compressed (trie_dna_optimized.py) = 888

FragileX-like Repetitive Sequence Memory Savings (aka using "Compressed" mode)

* Unoptimized (trie_dna.py) = 635480
* Optimized (trie_dna_optimized.py) = 571912
* Optimized Compressed (trie_dna_optimized.py) = 40176
```

The top series is for the larger set of sequences provided as an example. It shows that
the `__slots__`-based implementation can be easily reduced by almost half. The second
example shows a more complex example where CGG/CGN tri-allelic repeats are randomly
appended 50 times to represent a mutated individual that has Fragile X and a DNA
sequencer that gets confused by the GG repeats sometimes. 100 similar not identical
randomized sequences are combined in the trie. The repetitive sequence "compression"
notably reduces memory usage by over 90%!

You can see the source-code for implementation details and some notes. Here are
high-level optimizations that were done for the final results.


0. `__slots__` is still used same as before -- avoids the Python class `dict` overhead.
   This results in `Node` instances of 120 bytes being used for each node in the trie.

1. Use `int` as a terminal marker instead of a `Node` intance with `None` for all the
   possible children nodes. Results in 32 vs 120 bytes per terminal node in the trie.

2. Use `Node` vs `NodeWithCount` to drop the `count` internal var from objects that
   would always have a value of 0 for it. 88 vs 120 bytes per node

3. Use `NodeCompressed` to use a `sys.intern` string for non-branching paths through
   the trie. This saves substantial memory (~90%! in test CGG repeat regions)

   a. Non-branching paths used to be (N * 120) bytes where N = path length (aka
      number of nodes). `NodeCompressed` uses on the order of (120 + N) bytes

   b. `sys.intern` deduplicates memory usage for common strings. e.g. if `CGG` appears
      in many places in the graph, it is reduced to one instance in memory referenced
      by three different pointers.
