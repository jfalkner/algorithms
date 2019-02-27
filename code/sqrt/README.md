# Square Root

The [Square Root](https://en.wikipedia.org/wiki/Square_root) is a common math
function and most programming languages have a method for it, such as `sqrt` in
Python. It isn't particularly hard or interesting to calculate, but sets up
a code question that has easy followup questions about recursion and binary searching. 

Here is the problem:
 
> Make a the `sqrt` function that takes a number and returns an integer that
> equals the number when multiplied by itself. If no such integer exists, return
> the largest integer that when squared is still less than the number.
>
> For example, `sqrt(4)` is 2 and `sqrt(9)` is 3 and `sqrt(100)` is 10.
>
> More, largest int examples, `sqrt(5)` is 2 and `sqrt(10)` is 3.

### Solution

A brute force solution is to try all integers until one is too large, then back
off by one. This solution is O(N) runtime where N is num.

```python
def sqrt(num):
    for i in range(1, num):
        print('Checking %d' % num)
        i2 = i * i
        if i2 == num:
            return i
        elif i * i > num:
            return i - 1
```

Testing for `100` walks up to 10 and returns it.

```bash
Checking 100
Checking 100
Checking 100
Checking 100
Checking 100
Checking 100
Checking 100
Checking 100
Checking 100
Checking 100
10
```

#### Solution with Binary Search

[Binary Search](https://en.wikipedia.org/wiki/Binary_search_algorithm) is a
clever strategy to search a set of sorted items. The above brute force solution
to this problem is walking through a sorted list of integers, each increasing by
1. Why not binary search so that log2 integers are considered instead of all?

Below is both substantially faster at O(log(N)) runtime and it demonstrates
recursion, which is often asked about during code interviews.

```python
def sqrt(num):
    return bin_search(num, 1, num / 2)


def bin_search(num, min, max):
    print('Checking %d, min=%d, max=%d' % (num, min, max))
    i = int(min + (max - min) / 2)
    i2 = i * i
    if i2 == num:
        return i
    elif i2 > num:
        if min == max:
            return min - 1
        return bin_search(num, min, i)
    else:
        return bin_search(num, i if i != min else i + 1, max)
```

Searching for `sqrt(100)` now takes far fewer steps.

```bash
Checking 100, min=1, max=50
Checking 100, min=1, max=25
Checking 100, min=1, max=13
Checking 100, min=7, max=13
10
``` 

Likewise, a much bigger number takes far fewer steps too. For example, `sqrt(10000)`.

```bash
jayson@ubuntu:~/tokeep/.jfalkner/algorithms/code/sqrt$ python3 sqrt_binary.py 10000
Checking 10000, min=1, max=5000
Checking 10000, min=1, max=2500
Checking 10000, min=1, max=1250
Checking 10000, min=1, max=625
Checking 10000, min=1, max=313
Checking 10000, min=1, max=157
Checking 10000, min=79, max=157
Checking 10000, min=79, max=118
Checking 10000, min=98, max=118
Checking 10000, min=98, max=108
Checking 10000, min=98, max=103
100
```