from __future__ import annotations
from typing import Iterable

class File:
    def __init__(self, name, size):
        self._type = 'file'
        self.name = name
        self.size = size

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return 'File(%s)' % self.name

class Dir:
    def __init__(self, name, parent=False):
        self._type = 'dir'
        self.name: str = name
        self._size: int | bool = False
        self.parent: Dir = parent
        self.content: list[Dir | File] = []

    @property
    def size(self):
        if not self._size:
            self._compute_size()
        return self._size

    def __len__(self):
        return len(self.content)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return 'Dir(%s |%s)' % (self.name, len(self))

    def __iter__(self) -> Iterable:
        return iter(self.content)

    def __next__(self):
        for item in self.content:
            yield item
        raise StopIteration

    def _compute_size(self):
        self._size = sum(item.size for item in self.content)

    def add(self, item: Self | File):
        self.content.append(item)

    def get(self, name):
        for item in self.content:
            if name == item.name:
                return item
        raise Exception('File not found')

    def print(self, indent=0):
        for item in self:
            if isinstance(item, Dir):
                msg = '%s (dir)' % item
                print(msg.ljust(indent + len(msg), ' '))
                item.print(indent=indent + 1)
            else:
                msg = '%s (file, size=%s)' % (item, item.size)
                print(msg.ljust(indent + len(msg), ' '))

input_file = open('./2022/day07_input.txt')
commands = input_file.read().split('\n')
current_path = '/'

file_system: Dir = Dir('/')
current_dir: Dir = file_system

for i, cmd in enumerate(commands):
    if not cmd:
        continue
    if cmd.startswith('$'):
        if cmd == '$ ls':
            continue
        _, _, path = cmd.split()
        if path == '/':
            continue
        if path == '..':
            current_dir = current_dir.parent
        else:
            current_dir = current_dir.get(path)
    else:
        prefix, file_name = cmd.split()
        if prefix.isnumeric():
            # file
            current_dir.add(File(file_name, int(prefix)))
        else:
            # directory
            current_dir.add(Dir(file_name, parent=current_dir))

# Part 1
MAX_SIZE = 100000
def dfs(dir: Dir, size=0):
    if not dir:
        return 0
    if dir.size <= MAX_SIZE:
        size += dir.size
    for item in dir:
        if isinstance(item, Dir):
            size = dfs(item, size)
    return size

print('Part 1: %s' % dfs(file_system))

# Part 2
TOTAL_SIZE = 70_000_000
NEEDS_FREE = 30_000_000
TO_FREE = NEEDS_FREE - (TOTAL_SIZE - file_system.size)

def get_sizes(dir: Dir):
    res = [dir.size]
    for item in dir:
        if item._type == 'dir':
            res = res + get_sizes(item)
        
    return res

print('Part 2: %s' %
      sorted(filter(lambda size: size > TO_FREE, get_sizes(file_system)))[0])
