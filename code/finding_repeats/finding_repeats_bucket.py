import random

# start with randomized numbers and one duplicate
values = [1, 2, 3, 4, 5, 6, 7, 7, 8, 9, 10]
random.shuffle(values)
print(values)

# one pass through values and no hash collision time
counts = [0] * 101
for i in range(len(values) + 1):
    v = values[i]
    count = counts[v] + 1
    if count > 1:
        print(v)
        break
    counts[v] = count
