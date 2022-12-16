import sys
import time
from collections import deque
from copy import deepcopy


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


def bfs(start, target, valves):
    queue = deque()
    visited = {start}
    queue.append([start])
    while len(queue) > 0:
        curr_path = queue.popleft()
        last = curr_path[-1]
        neighbors_list = last.neighbors
        for neighbor_name in neighbors_list:
            neighbor = valves[neighbor_name]
            if neighbor not in visited:
                if target == neighbor:
                    return len(curr_path)
                new_path = curr_path.copy()
                new_path.append(neighbor)
                queue.append(new_path)
                visited.add(neighbor)
    return sys.maxsize


def do_leak(valves, count):
    global total_leak_value
    for valve in valves.values():
        if valve.open:
            valve.leak += valve.flow * count
            total_leak_value += valve.flow * count


def undo_leak(valves, count):
    global total_leak_value
    for valve in valves.values():
        if valve.open:
            valve.leak -= valve.flow * count
            total_leak_value -= valve.flow * count


def try_solve(timer, valves, current, cache):
    global total_leak_value, positive_flow_valves, open_valves
    key = Branch(timer, current.name, total_leak_value, valves)
    if key in cache.keys():
        return cache[key]
    if timer == 30:
        return total_leak_value
    max_total_leak = 0
    if open_valves == positive_flow_valves:
        # wait remaining time
        do_leak(valves, 30 - timer)
        max_total_leak = total_leak_value
        undo_leak(valves, 30 - timer)
    else:
       for neighbor_name in current.neighbors.keys():
            # go to neighbor and open it
            neighbor = valves[neighbor_name]
            if neighbor.flow == 0:
                continue
            neighbor_weight = current.neighbors[neighbor_name]
            if not neighbor.open and timer + neighbor_weight + 1 <= 30:
                do_leak(valves, neighbor_weight + 1)
                neighbor.open = True
                open_valves += 1
                leak = try_solve(timer + neighbor_weight + 1, valves, neighbor, cache)
                if leak > max_total_leak:
                    max_total_leak = leak
                neighbor.open = False
                open_valves -= 1
                undo_leak(valves, neighbor_weight + 1)
    cache[key] = max_total_leak
    return max_total_leak


total_leak_value = 0
open_valves = 0
positive_flow_valves = 0
lines = []
for line in sys.stdin:
    lines.append(line.strip())

valve_graph = dict()
reduced_valve_graph = dict()
for line in lines:
    parts = line.split(";")
    chunks1 = parts[0].split()
    name = chunks1[1]
    flow = int(chunks1[4].replace("rate=", ""))
    chunks2 = parts[1].replace("tunnels lead to valves", "").replace("tunnel leads to valve ", "").split(",")
    neighbor_dists = dict()
    for neighbor in chunks2:
        neighbor_dists[neighbor.strip()] = 1
    if flow > 0:
        reduced_valve_graph[name] = Valve(name, flow, dict())
        positive_flow_valves += 1
    valve_graph[name] = Valve(name, flow, neighbor_dists)

start = valve_graph["AA"]
reduced_valve_graph["AA"] = Valve(start.name, start.flow, dict())
for reduced_valve1 in reduced_valve_graph.values():
    for reduced_valve2 in reduced_valve_graph.values():
        if reduced_valve1 == reduced_valve2:
            continue
        dist = bfs(valve_graph[reduced_valve1.name], valve_graph[reduced_valve2.name], valve_graph)
        reduced_valve1.neighbors[reduced_valve2.name] = dist
        reduced_valve2.neighbors[reduced_valve1.name] = dist

# valves_copy = deepcopy(reduced_valve_graph)
start_time = time.time()
max_leak = try_solve(0, reduced_valve_graph, reduced_valve_graph["AA"], dict())
print("part1:", max_leak)
print("elapsed time [s]:", time.time() - start_time)
