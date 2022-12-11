import sys
from copy import deepcopy
from functools import reduce


class Monkey:
    def __init__(self, num, monkeys):
        self.num = num
        self.monkeys = monkeys
        self.checks = 0
        self.items = None
        self.operation = None
        self.divisible = None
        self.target_true = None
        self.target_false = None

    def with_items(self, items):    
        self.items = items
        return self
    
    def with_operation(self, operation):
        self.operation = operation
        return self
    
    def with_divisible_value(self, divisible):
        self.divisible = divisible
        return self
    
    def with_target_when_true(self, target_true):
        self.target_true = target_true
        return self
    
    def with_target_when_false(self, target_false):
        self.target_false = target_false
        return self

    def turn(self, modulo):
        for item in self.items:
            item = self.operation(item)
            if modulo != 0:
                item = item % modulo
            else:
                item = item // 3
            if item % self.divisible == 0:
                self.monkeys[self.target_true].items.append(item)
            else:
                self.monkeys[self.target_false].items.append(item)
            self.checks += 1
        self.items = []

    def __repr__(self):
        return "M(" + self.num + "), score= " + str(self.checks)


def build_operator(op, arg):
    if op == "+":
        return lambda x: x + int(arg)
    elif op == "*":
        if arg == "old":
            return lambda x: x * x
        else:
            return lambda x: x * int(arg)


lines = []
for line in sys.stdin:
    lines.append(line.strip())
monkeys = []
curr_monkey = None
modulo = 1
for line in lines:
    if line.startswith("Monkey"):
        chunks = line.split()
        curr_monkey = Monkey(chunks[0], monkeys)
    elif line.startswith("Starting items:"):
        line = line.replace("Starting items: ", "")
        chunks = line.split(",")
        item_list = []
        for chunk in chunks:
            item_list.append(int(chunk.strip()))
        curr_monkey.with_items(item_list)
    elif line.startswith("Operation:"):
        line = line.replace("Operation: new = old ", "")
        chunks = line.split()
        op = chunks[0]
        arg = chunks[1]
        curr_monkey.with_operation(build_operator(op, arg))
    elif line.startswith("Test: divisible by"):
        line = line.replace("Test: divisible by ", "")
        curr_monkey.with_divisible_value(int(line))
        modulo *= curr_monkey.divisible
    elif line.startswith("If true: throw to monkey "):
        line = line.replace("If true: throw to monkey ", "")
        curr_monkey.with_target_when_true(int(line))
    elif line.startswith("If false: throw to monkey "):
        line = line.replace("If false: throw to monkey ", "")
        curr_monkey.with_target_when_false(int(line))
    elif len(line) == 0:
        monkeys.append(curr_monkey)
monkeys.append(curr_monkey)

monkeys_copy = deepcopy(monkeys)
for i in range(20):
    for monkey in monkeys:
        monkey.turn(0)
sorted_monkeys = sorted(monkeys, key=lambda x: x.checks, reverse=True)
print("part1:", reduce(lambda x, y: x.checks * y.checks, sorted_monkeys[:2]))

monkeys = monkeys_copy
for i in range(10000):
    for monkey in monkeys:
        monkey.turn(modulo)
sorted_monkeys = sorted(monkeys, key=lambda x: x.checks, reverse=True)
print("part2:", reduce(lambda x, y: x.checks * y.checks, sorted_monkeys[:2]))


