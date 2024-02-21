# Calculator

There are various ways to ask recursive programming questions. One example is to ask for a candidate to create a simple calculator that can solve equations that include *, /, +, -. Precedence matters too. * and / should be evaluated before + and -.

I've been asked forms of this question from various interviews. It is more along the lines of a meatier problem to ask someone to solve in 30 minutes. Not because any of it is particularly hard, but because it has two distinct steps.

1. Parse the string to an equation (this largely uninteresting plumbing / FizzBuzz)
2. Calcuate the result of a parsed equation, respecting operator precedence

If you waste any time with the plumbing you'll short on time for doing the calculation. That is the trickier part that
needs a little CS thinking. A simple solution is to use recursion, albeit not the only solution.

Unlike other problems in this repository, this one usually doesn't have the standard runtime and memory sections at
the end. Correctness is usually the only goal.


### Example Equations

Here are some example equations. Always assume that inputs are correctly formatted -- no tricks there.

`1 + 2` simple, one operation. Answer `3`

`1 + 2 - 2` all the same precedence but more than 2 values to parse

`1 + 2 * 3` check precedence. Answer `7` aka `1 + 6`

`1 / 2 + 3` check that division keeps fractions and precedence. Answer `3.5` aka `0.5 + 3`

`1 + 2 / 2 * 3 + 4 / 2 - 1` longer equation with all operands, multiple use of similar operands and precedence. Answer
`5` aka `1 + 3 + 2 - 1`.

A sneaky thing to note is how `/` is handled. If we're doing division, does it matter if the fractions are kept and at
what precision? A reasonable requirement is that floating point precision is used. You can't keep everything as a string
all the time or you'll end up with some lossy string conversions.

### Example Algorithm

Below is an example algorithm for parsing a valid string to a list with respective parts of the equation still in order.
The doctest strings show expected output for the given string. Nothing fancy here. Mostly plumbing to convert a string
to the logical chunks of an equation.

```
"""
>>> parse_equation('1+2')
['1', '+', '2']

>>> parse_equation('1+2/3*4')
['1', '+', '2', '/', '3', '*', '4']
"""
def parse_equation(equation):
    """Parse out numbers and operators, keeping ordering"""
    equation_buf = []
    num_buf = []
    for c in equation:
        if c >= '0' and c <= '9':
            # Buffer this number. It might be a multi-digit number
            num_buf.append(c)
        else:
            # Append the full number
            equation_buf.append(''.join(num_buf))
            num_buf = []
            # Append the operator
            equation_buf.append(c)
    # Make sure that the last number is included
    equation_buf.append(''.join(num_buf))
    return equation_buf
```

Below is a method that takes a parsed equation and evaluates it. This is where some more creative thinking is required.
The equation needs to have operator precedence respected (* and / before + and -). An equation may have multiple of any
given operator too. For example:

* `1 * 2 + 3 * 4` could have (* and /) be done in one pass to make `2 + 12`, then (+ and -) to make `14`
* `1 * 2 * 3` is trickier because you need to know the result of `1 * 2` in order to multiply it by `3`. Not as easy to use just the parsed equation with a single pass.

Recursion is a good solution to generally solving the second bullet point. Work from left-to-right. After evaluating
an operator, make an updated parsed equation and call the same evaluation method again. The method can recursively call
itself as many times as needed.

Below is an example of such a recursive function. You could also directly manage a stack, if you wanted to keep this as
one function that doesn't need to call itself again.

```
"""
>>> calculate_equation(['1', '+', '2'])
3
"""
def calculate_equation(parsed_equation):
    """Recursively calculate the equation until done"""
    # Terminal condition
    if len(parsed_equation) == 1:
        return parsed_equation[0]

    # Handle higher precedence first
    for i, part in enumerate(parsed_equation):
        if part == '*' or part == '/':
            a = parsed_equation[i-1]
            b = parsed_equation[i+1]
            if part == '*':
                val = float(a) * float(b)
            else:
                val = float(a) / float(b)
            if i + 1 < len(parsed_equation):
                return calculate_equation([*parsed_equation[:i-1], val, *parsed_equation[i+2:]])
            else:
                return calculate_equation([*parsed_equation[:i-1], val])

    # Handle lower precedence second
    for i, part in enumerate(parsed_equation):
        if part == '+' or part == '-':
            a = parsed_equation[i-1]
            b = parsed_equation[i+1]
            if part == '+':
                val = float(a) + float(b)
            else:
                val = float(a) - float(b)
            if i + 1 < len(parsed_equation):
                return calculate_equation([*parsed_equation[:i-1], val, *parsed_equation[i+2:]])
            else:
                return calculate_equation([*parsed_equation[:i-1], val])
```

Note two other clever things in the above code. First, there are just two loops so that precedence is respected. The
first loop handles (* and /) and the second handles (+ and -). Second, the code uses `float()` to convert string
representations of number to floating point representation, and it keeps the float value in the parsed equation. This
avoids any float-to-string precision loss. It also is fine since calling `float()` on a float value works fine.

It works! You can try with examples such as the following.

```
def test_equation(equation, answer):
return f'{equation}={calculate_equation(parse_equation(equation))} expected {answer}'

print(test_equation('1+2', 3))
print(test_equation('1+2+3', 6))
print(test_equation('1*2+3*4', 15))
```

### Runtime and Memory Use

There isn't much to talk about here. The equation is parsed with a single pass thus `O(n)` where `n` is the length of
the equation string. Evaluation happens once per operator, which is again similar to `O(m)` where `m` is the number of
operators in the equation, which should end up being at most `n/2` since there are as many numbers as operators. Overall
runtime is something like `O(n) + O(n/2)` or generalized to `O(n)`.

Memory usage is minimal too. The example code makes new arrays that reuse existing values and calls itself recursively.
It is fair to say it should be constant memory usage; however, the recursion is on the stack. If the equation is huge,
you might run of stack memory -- hard to imagine that happening on modern computers. If you wanted to ensure constant,
non-growing memory use you could avoid using the stack and update the equation buffer in place.

In general, this algorithm question likely isn't being asked for the purposes of runtime and memory analysis. It is more
along the lines of seeing if you can get a correct technical solution.
