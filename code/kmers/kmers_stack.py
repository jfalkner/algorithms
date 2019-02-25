alphabet = ['A', 'C', 'T', 'G']


def kmer(length, prefix=''):
    if length == 0:
        yield prefix
    else:
        for c in alphabet:
            for v in kmer(length - 1, prefix + c):
                yield v
