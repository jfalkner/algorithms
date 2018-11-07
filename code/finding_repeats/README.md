# Finding Repeats

This example is similar to [FizzBuzz](../fizzbuzz/README.md), but is easy to
not think enough about and use default O(n log n) sorting. If you can assert
a few constraints, it can be O(n).

> You have a list of numbers that are in a random order. Only one number in the
> list appears twice. Find that number.

It is helpful to not over think an initial answer. If these items are sorted,
you can simply find what number appears twice. That works. Then pause to think
if O(n log n) can be dropped to O(n) or better.

I was asked this question by Duo Security during interviews. It seemed clearly
to be a FizzBuzz style question; however, the lead interviewer was also clearly
experienced. I suspected he wanted to check my communication skills and be
able to ask follow-up questions about the problem. The below solutions walk
through the discussion we had.

### Solution #1: Easy O(n log n)

Most languages readily let you sort anything with a common O(n log n) algorithm
such as mergesort, etc. Python 3 doesn't explicitly declare it, but `sorted` or
`.sort()` are it.

Sorting followed by a check for duplicates is the easy, not much though solution.

```python
import random

# start with randomized numbers and one duplicate
values = [1, 2, 3, 4, 5, 6, 7, 7, 8, 9, 10]
random.shuffle(values)
print(values)

# sort and show the duplicated value
values.sort()
for i in range(len(values)):
    if values[i] == values[i+1]:
        print(values[i])
        break
```

Output confirms that values are randomized and `7` is correctly picked out.

```bash
$ python3 finding_repeats.py 
[4, 6, 7, 2, 5, 7, 10, 1, 8, 3, 9]
7
```

Timing above (assume top part up to `print(values)` doesn't count) is O(n log n)
to sort `values` and then O(n) to find, thus O(n log n) overall. The sort is
in-place so memory use is O(1) if we don't have to count `values`.

### Solution #2: Map

A map is a good solution that drops the O(n log n) in favor of a single pass
through the list. O(n) for the single pass and O(1) for each map use, meaning
O(n) overall timing. O(n) space use.

A perk to using a map is that items need not be sortable. Just hashable and
comparable.

```python
# map values with a single pass and break on duplicate
counts = {}
for i in range(len(values) + 1):
    v = values[i]
    count = counts.get(v, 0) + 1
    if count > 1:
        print(v)
        break
    counts[v] = count
```

A subtle thing to point out is that maps can have collisions. It is usually
fair to assert maps are O(1) for get and put; however, a poorly implemented map
or an undersized map can be much slower. e.g. with a naive list lookup and size
of 1, the above map use ends up as O(n^2)

### Solution #3: Bucket

If you can assert some simple constraints, this problem can be guaranteed to be
O(n) with O(1) space. Assert that input are integers in a fixed range that is 
reasonable to keep in memory, such as 1-100.

The solution below is now O(n) since one pass is required and `counts` is just an
array -- no hash collisions possible. Memory use is O(1) because `counts`
doesn't change based on the size of the input.

```python
# one pass through values and no hash collision time
counts = [0] * 101
for i in range(len(values) + 1):
    v = values[i]
    count = counts[v] + 1
    if count > 1:
        print(v)
        break
    counts[v] = count
```