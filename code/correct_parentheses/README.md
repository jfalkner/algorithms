# Valid Parentheses

This example is similar to [FizzBuzz](../fizzbuzz/README.md), but masked a bit
by a programmer-friendly concept. Code doesn't compile if syntax isn't correct.

> Make a program that counts opening and closing parentheses. Note if the given
> syntax is valid or not. Valid means every opening paren has a closing, and
> a closing paren doesn't happen before an open.
>
> Valid = () or (()) or (()()) or (()(())), etc....
>
> Invalid = ( or ) or )( or ))(( or ())(

Important thing here is not to over think it. It is a simple problem and almost
certainly has a O(n) style solution. 

I was asked this during interviews at PacBio. It struck me as unusual given my 
10+ years of experience, my publications and talks, and lots complex code 
examples in GitHub. In any case, not much choice but to jump the hoop and also
not fair to assume interviewers have researched candidates.

### Solution

A single pass through while incrementing for an open and decrementing for a
close does it. If not at zero at the end, it isn't valid. If ever less than
zero, it isn't valid. O(n) time and O(1) memory use.

```python
import sys

def valid(line):
    i = 0
    for c in line:
        if c == '(':
            i += 1
        elif c == ')':
            i -= 1
        if i < 0:
            return False
    return i == 0

for line in sys.stdin:
    print('Valid' if valid(line) else 'Invalid')
```

Example output below.

```python
$ python3 correct_parentheses.py 
)
Invalid
))
Invalid
)(
Invalid
()
Valid
(())
Valid
(())(
Invalid
```