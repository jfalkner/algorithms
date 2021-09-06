"""
ptrie that is memory optimized to represent DNA sequences

This data structure is intended to keep a minimal memory representation of DNA sequences
and allow for querying what portion of the input sequences were accounted for by a set
of characters.

See trie_dna.py for the simple, non-optimized version. README.md better describes the
optimizations added to this version:

0. __slots__ is still used same as before -- avoids the Python class `dict` overhead

1. Use `int` as a terminal marker. 32 vs 120 bytes per terminal node in the trie.

2. Use `Node` vs `NodeWithCount` to drop the `count` internal var from objects that
   would always have a value of 0 for it. 88 vs 120 bytes per node

3. Use `NodeCompressed` to use a `sys.intern` string for non-branching paths through
   the trie. This saves substantial memory (~90%! in test CGG repeat regions)

   a. Non-branching paths used to be (N * 120) bytes where N = path length (aka
      number of nodes). `NodeCompressed` uses on the order of (120 + N) bytes

   b. `sys.intern` deduplicates memory usage for common strings. e.g. if `CGG` appears
      in many places in the graph, it is reduced to one instance in memory referenced
      by three different pointers.
"""
import sys
from collections import deque

class Node:
    """Prefix character that one or more sequences contained

    This and NodeWithCount are the bulk of the prefix data structure. Node is used by
    default since it lacks the `count` var and saves a little space. Node is upgraded
    to NodeWithCount if at least one sequence ends at a given node instance.
    """
    __slots__ = 'A', 'C', 'T', 'G', 'N'
    def __init__(self, A=None, C=None, G=None, T=None, N=None):
        self.A = A
        self.C = C
        self.G = G
        self.T = T
        self.N = N

class NodeWithCount:
    """Prefix character and ending character of one or more input sequences"""
    __slots__ = 'A', 'C', 'T', 'G', 'N', 'count'
    def __init__(self, A=None, C=None, G=None, T=None, N=None, count=0):
        self.A = A
        self.C = C
        self.G = G
        self.T = T
        self.N = N
        self.count = 0

class NodeCompressed:
    """Optimized representation of a non-branching path in the trie

    This replaces paths of non-branching Node instances during a one-time call to
    `_compress` after a trie is created. It can provide substantial memory savings
    since it converts many 120 byte objects (120 * N bytes) to a single object with a
    string (120 + N bytes).

    `sys.intern` is called on `sequence` to deduplicate the memory required to store
    strings representing identical non-branching paths occuring anywhere in the trie.
    """
    __slots__ = 'sequence', 'next'
    def __init__(self, sequence, next_node):
        self.sequence = sequence
        self.next = next_node

def _lazy_convert_and_increment_terminal(n):
    """Ensures the node is a class that can track count and increments the count

    Node doesn't have a count in order to save memory. If a sequence ends, then Node
    must be swapped to a NodeWithCount in order to track how many sequences ended on it.
    If no Node exists, then a terminal count (just an int) may be used.

    This method is only called on the last character of a sequence. The count always
    gets incremented here too.
    """
    if n:
        if not isinstance(n, NodeWithCount) and not isinstance(n, int):
            n = NodeWithCount(n.A, n.C, n.G, n.T, n.N)
        if isinstance(n, int):
            n += 1
        else:
            n.count += 1
    else:
        n = 1
    return n

def _lazy_convert_terminal(n):
    """Ensures the node allows for children nodes

    A terminal marker (an int) is used to represent the end of sequences since it
    saves memory. If a later sequence is added that requires children, the marker must
    be upgraded to an instance of NodeWithCount.
    """
    if n:
        if isinstance(n, int):
            n = NodeWithCount(count=n)
    else:
        n = Node()
    return n

def _lazy_compress(n, sequence):
    """Converts nodes with just one child to a compressed representation to save memory"""
    if isinstance(n, int):
        if len(sequence) > 1:
            return NodeCompressed(sys.intern(sequence), n)
        return n

    # only compress if there are no counts that'll be lost
    if not isinstance(n, NodeWithCount):
        if n.A and not any((n.C, n.G, n.T, n.N)):
            return _lazy_compress(n.A, sequence + 'A')
        if n.C and not any((n.A, n.G, n.T, n.N)):
            return _lazy_compress(n.C, sequence + 'C')
        if n.G and not any((n.A, n.C, n.T, n.N)):
            return _lazy_compress(n.G, sequence + 'G')
        if n.T and not any((n.A, n.C, n.G, n.N)):
            return _lazy_compress(n.T, sequence + 'T')
        if n.N and not any((n.A, n.C, n.G, n.T)):
            return _lazy_compress(n.N, sequence + 'N')

    # if just one character, there is nothing to compress
    if len(sequence) == 1:
        return n

    return NodeCompressed(sequence, n)

def _compress(n):
    """Reduces non-branching multi-Node paths to single NodeCompressed instances

    This method is intended to be run once after all words are added. It can save a
    large amount of space by converting non-branching N-length sequences from (120 * N)
    bytes to be <= (120 + N) bytes. These sequences can be anywhere in the graph.
    """
    if not n:
        return

    # depth-first heap-based recursion is used here to avoid running out of memory
    nodes = deque((n.A, n.C, n.G, n.T, n.N))

    while len(nodes):
        n = nodes.pop()

        # skip terminal markers
        if not n:
            continue;

        if not isinstance(n, int):
            if n.A and not isinstance(n.A, int) and not isinstance(n.A, NodeWithCount):
                n.A = _lazy_compress(n.A, 'A')
                nodes.append(n.A.next if isinstance(n.A, NodeCompressed) else n.A)
            if n.C and not isinstance(n.C, int) and not isinstance(n.C, NodeWithCount):
                n.C = _lazy_compress(n.C, 'C')
                nodes.append(n.C.next if isinstance(n.C, NodeCompressed) else n.C)
            if n.G and not isinstance(n.G, int) and not isinstance(n.G, NodeWithCount):
                n.G = _lazy_compress(n.G, 'G')
                nodes.append(n.G.next if isinstance(n.G, NodeCompressed) else n.G)
            if n.T and not isinstance(n.T, int) and not isinstance(n.T, NodeWithCount):
                n.T = _lazy_compress(n.T, 'T')
                nodes.append(n.T.next if isinstance(n.T, NodeCompressed) else n.T)
            if n.N and not isinstance(n.N, int) and not isinstance(n.N, NodeWithCount):
                n.N = _lazy_compress(n.N, 'N')
                nodes.append(n.N.next if isinstance(n.N, NodeCompressed) else n.N)


def add_word(trie, word):
    """Adds a word/sequence to the given trie"""
    # start at the root node and add each letter
    n = trie
    for i in range(len(word)):
        c = word[i]

        # if last character, use a terminal marker (an `int` of the count) to save space
        if i == len(word) - 1:
            if c == 'A':
                n.A = _lazy_convert_and_increment_terminal(n.A)
            if c == 'C':
                n.C = _lazy_convert_and_increment_terminal(n.C)
            if c == 'G':
                n.G = _lazy_convert_and_increment_terminal(n.G)
            if c == 'T':
                n.T = _lazy_convert_and_increment_terminal(n.T)
            if c == 'N':
                n.N = _lazy_convert_and_increment_terminal(n.N)
            break

        # Node is used by default to save the `count` internal var space
        if c == 'A':
            n.A = _lazy_convert_terminal(n.A)
            n = n.A
        if c == 'C':
            n.C = _lazy_convert_terminal(n.C)
            n = n.C
        if c == 'G':
            n.G = _lazy_convert_terminal(n.G)
            n = n.G
        if c == 'T':
            n.T = _lazy_convert_terminal(n.T)
            n = n.T
        if c == 'N':
            n.N = _lazy_convert_terminal(n.N)
            n = n.N

def make_trie(words, compress=True):
    """Create a trie from the given words (DNA sequences)

    It is assumed that each word consists of only A, C, G, T and N. No error handling
    for case sensitivity or unexpected characters is done.
    """
    n = Node()
    for word in words:
        add_word(n, word)
    if compress:
        _compress(n)
    return n

def tally(n, num_a=0, num_c=0, num_g=0, num_t=0, num_n=0):
    """Tallies the frequency of A, C, G, T and N via depth-first stack-based recursion"""
    # tally how many observations of prefixes up until now using NodeWithCount or terminal marker (an int)
    count = 0
    if isinstance(n, NodeWithCount):
        count = n.count
    elif isinstance(n, int):
        count = n
    tallies = (x * count for x in (num_a, num_c, num_g, num_t, num_n))

    # tally compressed sequences by adding up all characters
    if isinstance(n, NodeCompressed):
        for c in n.sequence[1:]:
            if c == 'A':
                num_a += 1
            if c == 'C':
                num_c += 1
            if c == 'G':
                num_g += 1
            if c == 'T':
                num_t += 1
            if c == 'N':
                num_n += 1
        tallies = map(sum, zip(tallies, tally(n.next, num_a, num_c, num_g, num_t, num_n)))

    elif isinstance(n, NodeWithCount) or isinstance(n, Node):
        if n.A:
            tallies = map(sum, zip(tallies, tally(n.A, num_a + 1, num_c, num_g, num_t, num_n)))
        if n.C:
            tallies = map(sum, zip(tallies, tally(n.C, num_a, num_c + 1, num_g, num_t, num_n)))
        if n.G:
            tallies = map(sum, zip(tallies, tally(n.G, num_a, num_c, num_g + 1, num_t, num_n)))
        if n.T:
            tallies = map(sum, zip(tallies, tally(n.T, num_a, num_c, num_g, num_t + 1, num_n)))
        if n.N:
            tallies = map(sum, zip(tallies, tally(n.N, num_a, num_c, num_g, num_t, num_n + 1)))

    return tallies


def calculate_fraction(trie, characters):
    """
    Does the main task of this programming challenge in one functional-style method.
    This also allows for doctest cases to be included that capture both given examples
    and some extra tests added for edge cases and optimizations.

    Run with `python -m doctest trie_dna_optimized.py`

    # edge case where no input is provided
    >>> calculate_fraction(make_trie([]), {'A'})
    Traceback (most recent call last):
     ...
    ValueError: Can not estimate frequency if no sequences are provided

    # very small trie to smoke test things
    >>> calculate_fraction(make_trie(['A', 'C', 'T', 'G']), {'A'})
    0.25

    # manually calculated test case #1 with 8/18 being C's or G's
    >>> calculate_fraction(make_trie(['ACTG', 'AACT', 'TCAGG', 'TTGGA']), {'G', 'C'})
    0.4444444444444444

    # same as above but confirming all is returned if all characters are considered
    >>> calculate_fraction(make_trie(['ACTG', 'AACT', 'TCAGG', 'TTGGA']), {'A', 'C', 'G', 'T'})
    1.0

    # manually calculated test case #2 with 16/30 being C's or G'
    >>> calculate_fraction(make_trie(['ACTG', 'AACT', 'TCAGG', 'ACTG', 'ACTG', 'GGCG', 'TTGGA']), {'C', 'G'})
    0.5333333333333333

    # manually calculated test case #3 with 32/35 being C's or G' checing "compression" logic via FragileX repeats
    >>> calculate_fraction(make_trie(['CGGCGGA', 'CGGCGGC', 'CGGCGGG', 'CGGCGGT', 'CGGCGGN']), {'C', 'G'})
    0.9142857142857143
    """
    # total of each character based on iterating through the trie
    num_a, num_c, num_g, num_t, num_n = tally(trie)

    numerator = sum(
        [x if y in characters else 0
         for (x, y) in [(num_a, 'A'), (num_c, 'C'), (num_g, 'G'), (num_t, 'T'), (num_n, 'N')]])
    denominator = sum((num_a, num_c, num_g, num_t, num_n))

    # return the fraction and protected against divide-by-zero
    if not denominator:
        raise ValueError("Can not estimate frequency if no sequences are provided")

    return numerator / denominator
