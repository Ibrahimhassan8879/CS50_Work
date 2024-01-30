# TODO
from cs50 import get_int

Height = get_int("Height: ")

while Height > 8 or Height <= 0:
    Height = get_int("Height: ")
spaces = Height - 1
hashes = 1


for i in range(Height):
    for j in range(spaces):
        print(' ', end="")
    for k in range(hashes):
        print('#', end="")
    hashes = hashes + 1
    spaces = spaces - 1
    print('')