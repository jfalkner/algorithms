"""Finds minimum number of coins to make change

A common phrasing of a dynamic programming problem that when framed with US
currency ends up solvable by a greedy algorithm. The sneaky tactic is to then
switch the currency values so that greedy won't work. e.g. make change for 6
using 1, 3 and 4 valued coins.
"""


def greedy_min_coins(amt, coins=0, values=[25, 10, 5, 1]):
    """Greedy algorithm for finding minimum coins to make change"""
    for value in values:
        if amt - value == 0:
            return coins + 1
        elif amt > value:
            return greedy_min_coins(amt - value, coins + 1)


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


def min_coins_recursion(amt, calcs=[], values=[4, 3, 1]):
    for v in values:
        if amt - v > 0:
            calcs.append((amt - v))
            min_coins_recursion(amt - v, calcs, values)
    return calcs
