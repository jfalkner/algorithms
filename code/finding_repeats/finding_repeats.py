import random

# start with randomized numbers and one duplicate
values = [1, 2, 3, 4, 5, 6, 7, 7, 8, 9, 10]
random.shuffle(values)
print(values)

# sort and show the duplicated value
values.sort()
for i in range(len(values)):
    if values[i] == values[i+1]:
        print(values[i])
        break