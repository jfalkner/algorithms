def sqrt(num):
    for i in range(1, num):
        print('Checking %d' % num)
        i2 = i * i
        if i2 == num:
            return i
        elif i * i > num:
            return i - 1


if __name__ == '__main__':
    import sys
    print(sqrt(int(sys.argv[1])))
