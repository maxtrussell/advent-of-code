import aoc

def insert_dir(fs, path, dir_name):
    pwd = path_lookup(fs, path)
    pwd[dir_name] = {}

def insert_file(fs, path, file_name, size):
    pwd = path_lookup(fs, path)
    pwd[file_name] = int(size)
    
def path_lookup(fs, path):
    pwd = fs
    for elem in path:
        pwd = pwd[elem]
    return pwd

dir_sizes = {}
def get_size(fs, path):
    if tuple(path) not in dir_sizes:
        pwd = path_lookup(fs, path)
        size = 0
        for k, v in pwd.items():
            if isinstance(v, int): 
                size += v
            else:
                size += get_size(fs, path + [k])
        dir_sizes[tuple(path)] = size
    return dir_sizes[tuple(path)]

fs = {'/': {}}
path = ['/']
for line in aoc.input_lines():
    tokens = line.split(' ')
    if tokens[0] == '$':
        # User command
        if tokens[1] == 'ls':
            continue

        arg = tokens[2]
        if arg == '/':
            path = ['/']
        elif arg == '..':
            path = path[:-1]
        else:
            path.append(arg)
    else:
        # ls data
        if tokens[0] == 'dir':
            dir_name = tokens[1]
            insert_dir(fs, path, dir_name)
        else:
            size, file_name = tokens
            insert_file(fs, path, file_name, size)

get_size(fs, ['/'])

# Part 1
part1 = sum(size for size in dir_sizes.values() if size < 100000)
print('Part 1: ', part1)

# Part 2
disk_size = 70000000
required_disk = 30000000
disk_usage = dir_sizes[('/',)]
remaining_disk = disk_size - disk_usage
to_delete = required_disk - remaining_disk
part2 = min(size for size in dir_sizes.values() if size >= to_delete)
print('Part 2: ', part2)
