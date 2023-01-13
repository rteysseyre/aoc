#!/usr/bin/env python3
# Raphaël Teysseyre, 2022

# Compute worry level modulo this number to avoid too-big numbers.
# This is the product of the modulo value of all monkeys
MODULO = 19 * 5 * 11 * 17 * 7 * 13 * 3 * 2

class Monkey:
    def __init__(self, worry_change_func, test_func, monkey_true_id,
                 monkey_false_id, starting_items = []):
        self.worry_change_func = worry_change_func
        self.test_func = test_func
        self.monkey_true_id = monkey_true_id
        self.monkey_false_id = monkey_false_id
        self.starting_items = starting_items
        self.reset()

    def push_item(self, worry_level):
        self.wait_list.append(worry_level)

    def reset(self):
        self.wait_list = self.starting_items.copy()
        self.item_count = 0

    def analyse_items(self, monkeys, worry_divide):
        for item in self.wait_list:
            new_worry = self.worry_change_func(item)
            if worry_divide:
                new_worry //= 3
            new_worry %= MODULO

            if self.test_func(new_worry):
                monkeys[self.monkey_true_id].push_item(new_worry)
            else:
                monkeys[self.monkey_false_id].push_item(new_worry)

            self.item_count += 1

        self.wait_list = []

monkeys = [
    Monkey(
        lambda x : x * 13,
        lambda x : x % 19 == 0,
        6, 2, [91, 66]),
    Monkey(
        lambda x : x + 7,
        lambda x : x % 5 == 0,
        0, 3, [78, 97, 59]),
    Monkey(
        lambda x : x + 6,
        lambda x : x % 11 == 0,
        5, 7, [57, 59, 97, 84, 72, 83, 56, 76]),
    Monkey(
        lambda x : x + 5,
        lambda x : x % 17 == 0,
        6, 0, [81, 78, 70, 58, 84]),
    Monkey(
        lambda x : x + 8,
        lambda x : x % 7 == 0,
        1, 3, [60]),
    Monkey(
        lambda x : x * 5,
        lambda x : x % 13 == 0,
        7, 4, [57, 69, 63, 75, 62, 77, 72]),
    Monkey(
        lambda x : x * x,
        lambda x : x % 3 == 0,
        5, 2, [73, 66, 86, 79, 98, 87]),
    Monkey(
        lambda x : x + 2,
        lambda x : x % 2 == 0,
        1, 4, [95, 89, 63, 67])]

def get_monkey_business(monkeys):
    most_active = []
    
    for m in monkeys:
        if len(most_active) == 0:
            most_active = [m]
            continue
    
        if len(most_active) == 1:
            if m.item_count > most_active[0].item_count:
                most_active = [m, most_active[0]]
            else:
                most_active = [most_active[0], m]
            continue
    
        if m.item_count > most_active[0].item_count:
            most_active = [m, most_active[0]]
            continue
    
        if len(most_active) == 1 or m.item_count > most_active[1].item_count:
            most_active = [most_active[0], m]

    return most_active[0].item_count * most_active[1].item_count

# Part 1
for r in range(20):
    for m in monkeys:
        m.analyse_items(monkeys, True)

print(get_monkey_business(monkeys))

# Part 2
for m in monkeys:
    m.reset()

for r in range(10000):
    for m in monkeys:
        m.analyse_items(monkeys, False)

print(get_monkey_business(monkeys))
