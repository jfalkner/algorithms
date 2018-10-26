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
