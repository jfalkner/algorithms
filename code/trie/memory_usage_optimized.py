"""
Helper script to compare memory usage of a ptrie, including memory optimizations
"""
import random

import trie_dna
import trie_dna_optimized

from pympler.asizeof import asized


# smaller test sequences that were verfied by hand
sequences = ['ACTG', 'AACT', 'TCAGG', 'ACTG', 'ACTG', 'GGCG', 'TTGGA']

unoptimized = trie_dna.make_trie(sequences)
optimized = trie_dna_optimized.make_trie(sequences, compress=False)
optimized_compressed = trie_dna_optimized.make_trie(sequences)


# mock up FragileX-like CGG repeats assuming some G's are miscalled as N's due to repeats
mostly_g = ['G', 'G', 'N']
repetitive_sequences = [
    ''.join(['CG' + random.choice(mostly_g) for x in range(50)])
    for x in range(100)
]

fx_unoptimized = trie_dna.make_trie(repetitive_sequences)
fx_optimized = trie_dna_optimized.make_trie(repetitive_sequences, compress=False)
fx_optimized_compressed = trie_dna_optimized.make_trie(repetitive_sequences)


print(f"""
Memory Usage Per Data Structure

* Unoptimized (trie_dna.py) = {asized(unoptimized).size}
* Optimized (trie_dna_optimized.py) = {asized(optimized).size}
* Optimized Compressed (trie_dna_optimized.py) = {asized(optimized_compressed).size}

FragileX-like Repetitive Sequence Memory Savings (aka using "Compressed" mode)

* Unoptimized (trie_dna.py) = {asized(fx_unoptimized).size}
* Optimized (trie_dna_optimized.py) = {asized(fx_optimized).size}
* Optimized Compressed (trie_dna_optimized.py) = {asized(fx_optimized_compressed).size}

""")
