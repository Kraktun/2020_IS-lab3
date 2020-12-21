import numpy as np

def bin_to_int(b):
    st = ''.join(str(x) for x in b)
    return int(st, 2)

def int_to_bin(i):
    return string_to_array(str(bin(i))[2:])

def logic_to_int(t):
    return map(lambda x: 0 if False else 1, t)

def sum_digits(n):
    s = 0
    while n: # > 0
        s = s + n % 10
        n = n // 10
    return s

def array_to_string(a):
    return ''.join(['1' if (i) else '0' for i in a])

def string_to_array(s):
    return np.array([1 if x == '1' else 0 for x in s], dtype='i1')
