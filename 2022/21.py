#!/usr/bin/env python3
# Raphaël Teysseyre, 2023

import re

operations = {}
for l in open('21_input'):
    name, op = l.strip().split(':')
    operations[name.strip()] = op.strip()

op = operations['root']

# Part 1. This is easy, thanks to eval()
while 1:
    variables = re.findall('[a-z]+', op)
    if len(variables) == 0:
        break
    for v in variables:
        op = op.replace(v, '(' + operations[v] + ')')

print(int(eval(op)))

# Part 2
# Create parse tree and simplify it

operations['root'] = operations['root'].replace('+', '==')
operations['humn'] = 'humn'

# Trial shows that 'humn' appears only once in the development of 'root'.
# This means that only one specific path in the parse tree cannot
# be computed without knowing 'humn'. Everything else can be computed
# without knowing 'humn'.

# Make one simplification pass. For every record in the operations dictionary,
# first try to convert to int. If we can't do that, we have an operation to
# compute. If both operands are int we can compute it, try to do that.
# Applying this function enough times will compute everything that can
# be computed in the parse tree without knowing 'humn'
def make_pass():
    for key in operations:
        if key == 'humn':
            continue

        try:
            operations[key] = int(operations[key])
            continue
        except:
            pass

        op = operations[key]
        variables = re.findall('[a-z]+', op)

        for v in variables:
            op = op.replace(v, '(' + str(operations[v]) + ')')

        try:
            operations[key] = int(eval(op))
        except:
            continue

for _ in range(50):
    make_pass()

lhs, rhs = operations['root'].split(' == ')
result = int(operations[rhs])

# Progressively simplify the root operation: the rhs is a known scalar,
# the lhs is always an operation between a scalar and a variable depending
# on humn. Perform the reverse operation on rhs/lhs to put all known values
# in the rhs until we get to 'humn' == <some scalar>
while lhs != 'humn':
    v1, op, v2 = operations[lhs].split()

    assert isinstance(operations[v1], int) or isinstance(operations[v2], int)
    assert op in ['+', '-', '*', '/']

    if op == '+':
        if isinstance(operations[v1], int):
            result -= operations[v1]
            lhs = v2
        else:
            result -= operations[v2]
            lhs = v1
    elif op == '-':
        if isinstance(operations[v1], int):
            result = operations[v1] - result
            lhs = v2
        else:
            result += operations[v2]
            lhs = v1
    elif op == '*':
        if isinstance(operations[v1], int):
            result //= operations[v1]
            lhs = v2
        else:
            result //= operations[v2]
            lhs = v1
    elif op == '/':
        # If this does not hold, we probably can't do integer math:
        assert isinstance(operations[v2], int)

        result *= operations[v2]
        lhs = v1

    result = int(result)

print('humn =', result)
