# k-mers (do you know recursion?)

[k-mer](https://en.wikipedia.org/wiki/K-mer) is a common question when asking
about recursion, and popular in fields such as genomics because human (and
other organisms) usually have their DNA represent as a string of nucleotides 
(aka A, C, T and Gs).

Regardless of the domain, this question is usually trying to tease out if you
understand recursion. A more subtle aspect is if the recursion relies on the
heap or the stack. 

Here is the problem:
 
> Make a method that'll create all unique strings of length k given an alphabet
> that is [A, C, T, G]. 
>
> For example, kmer(1) would return 'A', 'C', 'T', 'G'
>
> kmer(2) would return 'AA', 'AC', 'AT', 'AG', 'CA', 'CC', 'CT', ...

### Solution

The solution is just a few lines of code. It is O(A^K) where `A` is the size of
the alphabet and `K` is the length. Memory use is O(A + K) since the solution is
a depth first search that makes the longest string and returns it first.

```python
alphabet = ['A', 'C', 'T', 'G']


def kmer(length, prefix=''):
    if length == 0:
        yield prefix
    else:
        for c in alphabet:
            for v in kmer(length - 1, prefix + c):
                yield v
```

And output matches the example noted in the original question.

```bash
>>> [v for v in kmer(1)]
['A', 'C', 'T', 'G']
>>> [v for v in kmer(2)]
['AA', 'AC', 'AT', 'AG', 'CA', 'CC', 'CT', 'CG', 'TA', 'TC', 'TT', 'TG', 'GA', 'GC', 'GT', 'GG']
```

#### Heap vs Stack Recursion

Above is a stack-based recursion method. It relies on the programming language
remembering previous invocations of the kmer method and returning appropriately.
This is the most common style and it relies on the [stack](https://en.wikipedia.org/wiki/Stack-based_memory_allocation).

In short:

* Stack = first in first out (FIFO) storage that is commonly a contiguous region
  of memory space used to track thread state. Often visualized at the top or 
  beginning of RAM used by programs. In Python, see `sys.getrecursionlimit()`.
* Heap = random access portion of memory used to store data that is used and
  manipulated while the program runs. Limited by maximum available working
  memory (i.e. RAM plus page files minus stack-used memory). It is often
  visualized at the bottom of memory space and grows upward.
  
Usually stack is limited and will run out if very large amounts of recursion is
relied upon. You also can't persist the state of the stack in a program.

A nice tactic is to avoid relying on stack-based recursion and storing state
directly in the heap. This strategy works for any recursion. Below is a recast
of `kmer` that does that -- notice it does not call itself anymore.

```python
def kmer(length):
    prefix = ['']
    while len(prefix):
        p = prefix.pop()
        if len(p) == length:
            yield p
        else:
            prefix.extend([p + c for c in alphabet])
```

Output is the same as the other implementation. The main difference is that the
depth-first search is done by pushing prefixes to the `prefix` list and popping
off the longest ones until the desired `kmer` length is reached.

Above is a valid solution too! Arguably more flexible too since there is no
recursion limit (stack space limit) and, if you wanted, you could store `prefix`
to disk, database, or somewhere else, to pause the loop and resume it later.