# Making Change

A [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) 
question disguised in a simpler form. This is a common CS topic that
comes up during interviews. DP can reduce runtime dramatically. If you can split
a calculation into smaller ones and the same sub-calculation ends up repeated,
cache the answer and reuse it. Runtime is then on the order of how many
sub-problems exist.

For example, try making a method that can calculate the minimum coins needed to
make change for a currency. A US example would be using [1, 5, 10, 25] to make
change for up to 99 cents. 

You'd end up with input (amount) and output (# coins, coins_used) similar to the following:

* 52 cents = (4, [25, 25, 1, 1])
* 50 cents = (2, [25, 25])
* 6 cents = (2, [5, 1])
* 5 cents = (1, [5])
* 4 cents = (4, [1, 1, 1, 1])

This problem was first asked back in my CS undergrad coursework. It has an
intuitive greedy algorithm solution for US currency but quickly becomes a
dynamic programming question in order to support coins of any value. Because of
this it often ends up as an interview question that is fair to ask anyone and
scales well for more advanced programmers.

### Example Greedy Algorithm

Here is the greedy solution for the US currency example above. It is
important that the array is sorted so coins are in descending order.

```python
def greedy_min_coins(amt, coins=0, values=[25, 10, 5, 1]):
    """Greedy algorithm for finding minimum coins to make change"""
    for value in values:
        if amt - value == 0:
            return coins + 1
        elif amt > value:
            return greedy_min_coins(amt - value, coins + 1)
```

Running it with the initial examples gives the same answers.

```python
>>> greedy_min_coins(52)
4
>>> greedy_min_coins(50)
2
>>> greedy_min_coins(6)
2
>>> greedy_min_coins(5)
1
>>> greedy_min_coins(4)
4
```

Above runs in O(n) time where n the number of coins; however, easy to argue it
is O(1) since we know the max input is 99 and O(99) turns in to O(1). Fixed
space use too -- pretty good!

It'd be nice to see the coins used. Not tough to add and it'll be shown in the 
next example. 

The tricky thing is that this algorithm fails if a currency has
`values=[4, 3, 1]` and you have to make change for 6. The above strategy fails
since it'll pick 3 coins `[4, 1, 1]` but 2 is optimal `[3, 3]`.

```python
>>> greedy_min_coins(6, values=[4, 3, 1])
3
```

### Example Dynamic Programming Algorithm

The complication of this newly given currency is that it forces considering all
combinations of coins. In the worst case, something closer to O(m^n) where m is
the number of coins in the currency and n is the number of coins used to make
change. The greedy approach won't work for all cases.

3^n is an example based on this `[4, 3, 1]` set of coins. Given an amount, you
need to try subtracting each coin from it and recursively doing the same on the
resulting amount. The best option is whatever set has fewest coins and makes
exact change.

Above starts to sound a lot like a dynamic programming problem. If you draw out
the tree of combinations, you'll notice that the same sub-problem repeats. Here
is the O(3^n) recursion that tracks how many times an `amt` is repetitively
calculated.

```python
def min_coins_recursion(amt, calcs=[], values=[4, 3, 1]):
    for v in values:
        if amt - v > 0:
            calcs.append((amt - v))
            min_coins_recursion(amt - v, calcs, values)
    return calcs
```

For a smaller number such as 6, it ends up calculating optimal change for 2 four
times and optimal change for 3 twice.

```python
>>> from collections import Counter
>>> Counter(min_coins_recursion(6)).most_common()
[(1, 6), (2, 4), (3, 2), (4, 1), (5, 1)]
```

Bigger numbers explode in repetitive calculation. For example, 12.

```python
>>> Counter(min_coins_recursion(12)).most_common()
[(1, 110), (2, 68), (3, 42), (4, 26), (5, 16), (6, 9), (7, 6), (8, 4), (9, 2), (10, 1), (11, 1)]
```

A solution strategy is to cache results the first time the method is invoked for
each `amt` and smartly return the cache. This will only calculate each amount
from 1 up to the `amt` once. Given that phrasing, you can alternatively code a
solution that does the 1 to `amt` calc up front. Since you'll know the minimal
amount of coins for each smaller value, larger values can incrementally look up
the smaller value for each of the possible coin options -- keeping the min.

```python
def min_coins(amt, values=[4, 3, 1]):
    """Dynamic programming to minimum coins to make change"""
    coins = [0] * (amt + 1)
    for i in range(1, amt + 1):
        vals = [coins[i - v] + 1 for v in values if v <= i]
        min_coins = min(vals)
        coins[i] = min_coins
    return coins[amt]
```

Above give the expected answer of 2 for `min_coins(6)`.

Extending above to also show the coins use requires tracking what coin was added
during each incremental step. You can then decrement that coin and repeat with 
the leftover value until you know all coins used.

```python
def min_coins(amt, values=[4, 3, 1]):
    """Dynamic programming to minimum coins to make change"""
    coins = [0] * (amt + 1)
    coin_used = [0] * (amt + 1)
    for i in range(1, amt + 1):
        vals = [(coins[i - v] + 1, v) for v in values if v <= i]
        min_coins, coin_val = min(vals)
        coins[i] = min_coins
        coin_used[i] = coin_val

    # calculate what coins were used
    _amt = amt
    _used = []
    for i in range(coins[amt]):
        _used.append(coin_used[_amt])
        _amt = _amt - coin_used[_amt]

    return coins[amt], _used
```

Now the output is both optimal and shows what coins where used.

```python
>>> min_coins(6)
(2, [3, 3])
>>> min_coins(10)
(3, [3, 3, 4])
```

Above is also substantially better than 3^n. It is O(n) where n is amt. One
calculation and lookup is done for each step. Finding what coins were used is
worst case O(n), meaning overall calc and lookup is still just O(n). Space is
linear with n too. If we can set an upper limit on `amt`, say 99 cents like with
US currency, then the solution is arguably O(1) by similar logic as the greedy
algorithm.