# Values in Ranges

This is a problem with a relatively simple description that requires some clever thinking and use of binary searching to solve in less than quadratic time. I've seen this question discouraged from being used since you need to puzzle out the computer science (CS) tactics need to solve it, which is argued both unfair to candidates and not really related to actual work. I've also seen it purposely picked because it needs needs CS tricks to be done well but the naive solution isn't hard to make.

The challenge is to take a list of values and count how many end up in a list of different ranges. For example:

```
# values
[2, 4, 5, 6, 9, 11, 3, 1]

# Ranges [low, high] inclusive
[0, 3]  # has 3 values [1, 2, 3]
[2, 10] # has 6 values [2, 3, 4, 5, 6, 9]
[6, 20] # hash 3 values [6, 9, 11]
```

Notice that multiple ranges can match the input values and values can be in any order. Generally, assume that any big number can be used in a value and you may have many ranges.

### Iterative Solution (Sub-Optimal)

A seemingly straight-forward solution would be to iterate over the values and keep a count for each range, tracking how many values match it. This ends up being relatively slow since you are looping per value, per range and doing an increment per value too.

```
values = [2, 4, 5, 6, 9, 11, 3, 1]

# Ranges [low, high] inclusive
ranges = [
  [0, 3],
  [2, 10],
  [6, 20],
]

# Keep a count per range
range_counts = [0] * len(ranges)

# O(n) loop where n is the number of values
for value in values:
    # O(m) loop where m is the number of ranges
    for i, range in enumerate(ranges):
        low, high = ranges[i]
	# O(1) increment per value
        if value >= low and value <= high:
	    range_counts[i] += 1
```

Tests for the above code usually include the following tricks:
* Easy to pass. Above works for these.
   * Small examples like in the description.
   * Big values. Values are large eough numbers that you can't buket sort, or similar tricks.
   * Unsorted values. Any assumptions about values always incrementing or similar are broken.
   * Overalapping Ranges. Values match more than one given range.
* Harder to pass. Needs some clever algorithm usage
   * Really big nubmer of values (n in the above). Takes too long to run, based on some arbitrary limit the test has (e.g. 10 seconds)
   * Really big number of ranges (m in the above). Similar timeout issue.

### Binary Searching (Optimal Solution)

An more optimal solution for this challenge is to realize that you can do sub-quadratic time by first sorting the input then using a binary search to find two indexes per range: what value matches the lowest in the range and what value is the highest. Given the indexes, you can then simply calculate how many values are between (high - low + 1).

```
import bisect

values = [2, 4, 5, 6, 9, 11, 3, 1]
# In-place sort to ensure ascending order
values.sort()

# Ranges [low, high] inclusive
ranges = [
  [0, 3],
  [2, 10],
  [6, 20],
]

# O(m) loop where m is the number of ranges
for i, range in enumerate(ranges):
    low, high = ranges[i]
    low_index = bisect.bisect_left(values, low)
    high_index = bisect.bisect_right(values, high)
    # Directly calculate and display the count
    print(high_index - low_index)
```

Execution time works out to be n * log(n) + m * 2 log(n) or generalized to n * log(n) + m * log(n).
* n log(n) sort time -- where n is the number of input values
* m loops where m is the number of ranges
* log(n) lookup of lowest value index
* log(n) lookup of highest value index

This is much faster than the initial solution for cases with lots of input values or lots of ranges. 

Memory usage is essentially nothing extra. The input values can be sorted in place. Values to be outputted can be directly calculated and printed -- no need to store counts. 
