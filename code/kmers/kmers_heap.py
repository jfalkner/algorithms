alphabet = ['A', 'C', 'T', 'G']


def kmer(length):
    prefix = ['']
    while len(prefix):
        p = prefix.pop()
        if len(p) == length:
            yield p
        else:
            prefix.extend([p + c for c in alphabet])
