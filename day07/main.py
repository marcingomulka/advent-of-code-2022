import sys


class Node:
    def __init__(self, name, size, subdirs, files, parent):
        self.name = name
        self.size = size
        self.subdirs = subdirs
        self.files = files
        self.parent  = parent


def get_subdir(name, curr_node):
    for subdir in curr_node.subdirs:
        if subdir.name == name:
            return subdir
    return None


def execute_command(cmd, arg, curr_node, root):
    if cmd == "cd":
        if arg == '/':
            return root
        elif arg == '..':
            return curr_node.parent
        else:
            return get_subdir(arg, curr_node)


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
    for subdir in root.subdirs:
        print_tree(subdir, level + 1)


def calculate_sizes(node, path, dir_sizes):
    children_size = 0
    path += "/"
    path += node.name
    for subdir in node.subdirs:
        children_size += calculate_sizes(subdir, path, dir_sizes)
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

tree = Node("/", 0, [], set(), None)
curr_node = tree
for line in lines:
    chunks = line.split()
    if line.startswith("$"):
        if chunks[1] == "cd":
            cmd = chunks[1]
            arg = chunks[2]
            curr_node = execute_command(cmd, arg, curr_node, tree)
    elif line.startswith("dir"):
        sub_dir_name = chunks[1]
        if get_subdir(sub_dir_name, curr_node) is None:
            sub_dir = Node(sub_dir_name, 0, [], set(), curr_node)
            curr_node.subdirs.append(sub_dir)
    else:
        filename = chunks[1]
        file_size = int(chunks[0])
        if filename not in curr_node.files:
            curr_node.size += file_size
            curr_node.files.add(filename)

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

