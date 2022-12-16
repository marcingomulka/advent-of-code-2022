import sys
from queue import PriorityQueue


class Branch:
    def __init__(self, timer, cur, total, valves):
        self.timer = timer
        self.cur = cur
        self.total = total
        self.states = ""
        for valve in valves.values():
            if valve.open:
                self.states += "1"
            else:
                self.states += "0"

    def __hash__(self):
        return hash((self.timer, self.cur, self.total, self.states))

    def __eq__(self, other):
        return self.timer == other.timer and self.cur == other.cur and self.total == other.total and self.states == other.states




class Valve:
    def __init__(self, name, flow, neigbors):
        self.name = name
        self.flow = flow
        self.neighbors = neigbors
        self.open = False
        self.leak = 0

    def __repr__(self):
        return self.name + ", flow=" + str(self.flow) + ", connected=" + str(self.neighbors)


# def get_leak(valves):
#     leak = 0
#     for valve in valves.values():
#         leak += valve.leak
#     return leak


def do_leak(valves):
    global total_leak_value
    for valve in valves.values():
        if valve.open:
            valve.leak += valve.flow
            total_leak_value += valve.flow


def undo_leak(valves):
    global total_leak_value
    for valve in valves.values():
        if valve.open:
            valve.leak -= valve.flow
            total_leak_value -= valve.flow


# def all_open(valves):
#     all = True
#     for valve in valves.values():
#         if not valve.open and valve.flow > 0:
#             all = False
#             break
#     return all


def try_solve(timer, valves, current, cache):
    global total_leak_value, good_valves, open_valves
    key = Branch(timer, current.name, total_leak_value, valves)
    #print("time", timer, "visit", current.name)
    if key in cache.keys():
        return cache[key]
    if timer >= 30:
        return total_leak_value
    max_total_leak = 0
    for i in range(2):
        #decision open valve or go to neighbor or wait if all open
        if i == 0 and current.flow > 0 and not current.open:
            do_leak(valves)
            current.open = True
            open_valves += 1
            #print("open", current.name)
            leak = try_solve(timer + 1, valves, current, cache)
            if leak > max_total_leak:
                max_total_leak = leak
            current.open = False
            open_valves -= 1
            undo_leak(valves)
            #print("close", current.name)
        elif i == 1 and open_valves != good_valves:
            for neighbor_name in current.neighbors:
                neighbor = valves[neighbor_name]
                do_leak(valves)
                #print(current.name, "->", neighbor.name)
                leak = try_solve(timer + 1, valves, neighbor, cache)
                if leak > max_total_leak:
                    max_total_leak = leak
                #else:
                #    pruned.add(Branch(timer + 1, neighbor.name, valves))
                undo_leak(valves)
        elif i == 1 and open_valves == good_valves:
            do_leak(valves)
            leak = try_solve(timer + 1, valves, current, cache)
            if leak > max_total_leak:
                max_total_leak = leak
            undo_leak(valves)
    cache[key] = max_total_leak
    #print("max", max_total_leak)
    return max_total_leak


total_leak_value = 0
open_valves = 0
good_valves = 0
lines = []
for line in sys.stdin:
    lines.append(line.strip())

valves = dict()
for line in lines:
    parts = line.split(";")
    chunks1 = parts[0].split()
    name = chunks1[1]
    flow = int(chunks1[4].replace("rate=", ""))
    chunks2 = parts[1].replace("tunnels lead to valves", "").replace("tunnel leads to valve ", "").split(",")
    neighbor_names = []
    for neighbor in chunks2:
        neighbor_names.append(neighbor.strip())
    if flow > 0:
        good_valves += 1
    valves[name] = Valve(name, flow, neighbor_names)

current = valves["AA"]
total_leak = try_solve(0, valves, current, dict())
print("part1:", total_leak)
