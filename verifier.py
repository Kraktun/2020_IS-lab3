import numpy as np
from utils import *

class Verifier:
    
    def __init__(self, n = 0):
        self.counter = n
        self.shared_key = -1

    def get_challenge(self, lc):
        self.counter += 1
        self.c = np.random.choice(2, lc, p=[0.5, 0.5])
        return self.c, self.counter
    
    def verify_encryption(self, r):
        r_p = build_response(self.shared_key, self.c, self.counter)
        return (r_p == r).all()

def build_response(key, c, n):
    c_dec = bin_to_int(c)
    sc = sum_digits(c_dec)
    n_bin = int_to_bin(n)
    t_key = key
    # padding?
    if len(t_key) < len(n_bin):
        pad = len(n_bin) - len(t_key)
        t_key = np.pad(t_key, (pad, 0), 'constant', constant_values=(0))
    elif len(t_key) > len(n_bin):
        pad = len(t_key) - len(n_bin)
        n_bin = np.pad(n_bin, (pad, 0), 'constant', constant_values=(0))
    t = np.logical_xor(t_key, n_bin)
    t = logic_to_int(t)
    st = sum_digits(bin_to_int(t))
    s = sc*st
    return int_to_bin(s)