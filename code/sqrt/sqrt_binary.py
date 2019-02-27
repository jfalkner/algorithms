def sqrt(num):
    return bin_search(num, 1, num / 2)


def bin_search(num, min, max):
    print('Checking %d, min=%d, max=%d' % (num, min, max))
    i = int(min + (max - min) / 2)
    i2 = i * i
    if i2 == num:
        return i
    elif i2 > num:
        if min == max:
            return min - 1
        return bin_search(num, min, i)
    else:
        return bin_search(num, i if i != min else i + 1, max)


if __name__ == '__main__':
    import sys
    print(sqrt(int(sys.argv[1])))
