"""
See `trie_dna_optimized.py` for the final solution and README.md in this directory.

This was an initial implementation to proof-of-concept a trie using `__slots__` in
Pythong for some memory efficiency. The code came together so quickly that I stashed a
copy (this file) and used the rest of time to layer one several more substantial memory
savings in `trie_dna_optimized.py`
"""

class Node:
    """Prefix character that one or more sequences contained

    This is used to represent the entire trie. It can have children Node(s), one per 
    allowed character in the supported alphabet. Each Node has a `count` to track how
    many input sequences ended on the node. This is later used to calculate frequency
    of input characters.
    """
    __slots__ = 'A', 'C', 'T', 'G', 'N', 'count'
    def __init__(self, A=None, C=None, G=None, T=None, N=None):
        self.A = A
        self.C = C
        self.G = G
        self.T = T
        self.N = N
        self.count = 0

def add_word(trie, word):
    """Adds a word to the given trie"""
    # start at the root node and add each letter
    n = trie
    for c in word:
        if c == 'A':
            n.A = n.A if n.A else Node()
            n = n.A
        if c == 'C':
            n.C = n.C if n.C else Node()
            n = n.C
        if c == 'G':
            n.G = n.G if n.G else Node()
            n = n.G
        if c == 'T':
            n.T = n.T if n.T else Node()
            n = n.T
        if c == 'N':
            n.N = n.N if n.N else Node()
            n = n.N
    n.count += 1

def make_trie(words):
    """Makes a trie from a list of words/sequences"""
    n = Node()
    for word in words:
        add_word(n, word)
    return n

def tally(n, num_a=0, num_c=0, num_g=0, num_t=0, num_n=0):
    """Tallies character frequency via depth-first stack-based recursion"""
    # tally how many observations of prefixes up until now
    # Node and NodeTerminal can be tallied by count
    if isinstance(n, Node) or isinstance(n, NodeTerminal):
        tallies = (x * n.count for x in (num_a, num_c, num_g, num_t, num_n))

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
    Calculates the main feature for the challenge: fraction of characters from the input
    sequence. See `trie_dna_optimized.py` for more test and better empty trie error
    reporting.

    # edge case where no input is provided
    >>> calculate_fraction(make_trie([]), {'A'})
    0

    # very simple test case with a tiny trie
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
    """
    # total of each character based on iterating through the trie
    num_a, num_c, num_g, num_t, num_n = tally(trie)

    numerator = sum(
        [x if y in characters else 0
         for (x, y) in [(num_a, 'A'), (num_c, 'C'), (num_g, 'G'), (num_t, 'T'), (num_n, 'N')]])
    denominator = sum((num_a, num_c, num_g, num_t, num_n))

    # return the fraction and protected against divide-by-zero
    return numerator / denominator if denominator else 0
