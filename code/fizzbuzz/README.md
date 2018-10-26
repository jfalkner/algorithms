# FizzBuzz (aka can you program?)

[FizzBuzz](https://en.wikipedia.org/wiki/Fizz_buzz) is arguably the original way
to ask, "can you code at all?". The tactic of an easy program is surprisingly
common because, more surprisingly, the majority of applicants for a programming
job can't do this. Many will similarly fail to impress because they'll grossly
over-think it and fail to realize all that is needed is a few lines of code.

I first encountered this problem at Dow, and discussion of it comes up all the
time when talking about hiring and pre-screening to optimize time spent with
on-site interviews.

Here is the problem:
 
> Count incrementally, replacing any number divisible by three with the word
> "fizz", and any number divisible by five with the word "buzz".
>
> Make a program that does this from 1 to 100.

### Solution

The solution is just a few lines of code. It is O(n) time and O(1) space, no 
recursion, no caching and nothing fancy to talk about at all.

```python
for i in range(1, 101):
    if not i % 3:
        print('Fizz')
    elif not i % 5:
        print('Buzz')
    else:
        print(i)
```

And output matches Wikipedia's example.

```bash
$ python fizzbuzz.py 
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
...
```