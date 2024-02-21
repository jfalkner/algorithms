
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


if __name__ == '__main__':
    def test_equation(equation, answer):
        return f'{equation}={calculate_equation(parse_equation(equation))} expected {answer}'

    print(test_equation('1+2', 3))
    print(test_equation('1+2+3', 6))
    print(test_equation('1*2+3*4', 15))
