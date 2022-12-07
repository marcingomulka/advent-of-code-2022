import sys


class Node:
    def __init__(self, name, size, children, parent):
        self.name = name
        self.size = size
        self.children = children
        self.parent  = parent


def get_child(name, curr_node):
    for child in curr_node.children:
        if child.name == name:
            return child
    return None


def execute_command(cmd, arg, curr_node, root):
    if cmd == "cd":
        if arg == '/':
            return root
        elif arg == '..':
            return curr_node.parent
        else:
            return get_child(arg, curr_node)


def print_tree(root, level):
    prefix = ""
    for i in range(level):
        prefix += " "
    output = ""
    output += prefix
    output += root.name
    output += ":"
    output += str(root.size)
    print(output)
    for child in root.children:
        print_tree(child, level + 1)


def calculate_sizes(node, path, dir_sizes):
    children_size = 0
    path += "/"
    path += node.name
    for child in node.children:
        children_size += calculate_sizes(child, path, dir_sizes)
    node.size += children_size
    dir_sizes[path] = node.size
    return node.size


def get_p1_result(dir_sizes):
    sum = 0
    for size in dir_sizes.values():
        if size <= 100000:
            sum += size
    return sum


def get_p2_result(sorted_sizes, to_free):
    result = 0
    for dir_size in sorted_sizes:
        if dir_size >= to_free:
            result = dir_size
            break
    return result


lines = []
for line in sys.stdin:
    lines.append(line.strip())

tree = Node("/", 0, [], None)
curr_node = tree
for line in lines:
    chunks = line.split()
    if line.startswith("$"):
        if line.startswith("$ cd"):
            cmd = chunks[1]
            arg = chunks[2]
            curr_node = execute_command(cmd, arg, curr_node, tree)
    elif line.startswith("dir"):
        sub_dir_name = chunks[1]
        sub_dir = Node(sub_dir_name, 0, [], curr_node)
        curr_node.children.append(sub_dir)
    else:
        file_size = int(chunks[0])
        curr_node.size += file_size

dir_sizes = dict()
calculate_sizes(tree, "file://", dir_sizes)
#print_tree(tree, 0)
print("part1: ", get_p1_result(dir_sizes))

total = tree.size
target_unused = 70000000 - total
to_free = 0
if target_unused < 30000000:
    to_free = 30000000 - target_unused

sorted_sizes = list(dir_sizes.values())
sorted_sizes.sort()
print("part2: ", get_p2_result(sorted_sizes, to_free))

