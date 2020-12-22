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
    
    def verify_u3(self, r):
        r_p = build_response(self.shared_key, self.c, self.counter)
        return bin_to_int(r) == bin_to_int(r_p), r_p
        #return (r_p == r).all()

def build_response(key, c, n):
    c_dec = bin_to_int(c)
    sc = sum_digits(c_dec)
    t_key = bin_to_int(key)
    t = t_key + n
    st = sum_digits(t)
    s = sc*st
    return int_to_bin(s)
