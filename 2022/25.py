#!/usr/bin/env python3
# Raphaël Teysseyre, 2023

import math

SNAFU_VALS = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2
}

SNAFU_LOOKUP = {
    -2 : '=',
    -1 : '-',
    0 : '0',
    1 : '1',
    2 : '2'
}

# Convert SNAFU number to integer.
def snafu2int(s):
    exponent = 0
    out = 0
    for c in reversed(s.strip()):
        assert c in SNAFU_VALS
        out += SNAFU_VALS[c] * (5 ** exponent)
        exponent += 1
    return out

# Convert integer to SNAFU representation.
def int2snafu(i):
    assert i >= 0
    
    if i == 0:
        return '0' # Avoid computing log(0) below

    # Convert number to base 5
    base_5 = [0] # Resulting vector of digits. Prime with a leading zero.
    for exponent in reversed(range(1 + int(math.log(i)/math.log(5)))):
        digit = 0
        while i >= 5 ** exponent:
            digit += 1
            i -= 5 ** exponent
        base_5 = [digit] + base_5

    # Digits 3 and 4 don't exist in SNAFU.
    # When encountering one of those digits, add one
    # to the next digit and substract 5 from the
    # current digit (which becomes negative). Note that
    # we can get to a digit equal to 5 in this case, which
    # is ok. It will be set to zero and one will be added
    # to the next digit. We can't get to more than 5.
    # Example:
    # 2444 -> 245- -> 250- -> 300- -> 1=00-
    for x in range(len(base_5)):
        if base_5[x] > 2:
            base_5[x + 1] += 1
            base_5[x] -= 5

    # Remove leading zero if it was not replaced by
    # the above SNAFU conversion
    if base_5[-1] == 0:
        del base_5[-1]

    # Converts digits from [-2 .. 2] interval to SNAFU characters
    return ''.join([SNAFU_LOOKUP[d] for d in reversed(base_5)])

count = 0
for l in open('25_input'):
    count += snafu2int(l)

print(int2snafu(count))
