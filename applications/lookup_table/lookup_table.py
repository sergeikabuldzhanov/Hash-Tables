import math
import random
lookup = {}

def slowfun(x, y):
    # TODO: Modify to produce the same results, but much faster
    key = f"{x} {y}"
    if key in lookup:
        return lookup[key]
    v = math.pow(x, y)
    v = math.factorial(v)
    v //= (x + y)
    v %= 982451653

    return v

for x in range(2, 14):
    for y in range(3, 6):
        lookup[f"{x} {y}"] = slowfun(x, y)


# Do not modify below this line!

for i in range(50000):
    x = random.randrange(2, 14)
    y = random.randrange(3, 6)
    print(f'{i}: {x},{y}: {slowfun(x, y)}')
