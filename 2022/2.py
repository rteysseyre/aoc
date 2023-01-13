#!/usr/bin/env python3
# Raphaël Teysseyre, 2022

# Scoring for part 1
scores1 = {
    'A': { # Rock
        'X': 1 + 3, # Rock
        'Y': 2 + 6, # Paper
        'Z': 3 + 0, # Scissors
    },
    'B': { # Paper
        'X': 1 + 0, # Rock
        'Y': 2 + 3, # Paper
        'Z': 3 + 6, # Scissors
    },
    'C': { # Scissors
        'X': 1 + 6, # Rock
        'Y': 2 + 0, # Paper
        'Z': 3 + 3, # Scissors
    }
}

# Scoring for part 2
scores2 = {
    'A': { # Rock
        'X': 0 + 3, # Scissors
        'Y': 3 + 1, # Rock
        'Z': 6 + 2, # Paper
    },
    'B': { # Paper
        'X': 0 + 1, # Rock
        'Y': 3 + 2, # Paper
        'Z': 6 + 3, # Scissors
    },
    'C': { # Scissors
        'X': 0 + 2, # Paper
        'Y': 3 + 3, # Scissors
        'Z': 6 + 1, # Rock
    }
}

total1 = 0
total2 = 0

for line in open('2_input'):
    total1 += scores1[line[0]][line[2]]
    total2 += scores2[line[0]][line[2]]

print(total1)
print(total2)
    
