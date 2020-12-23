import numpy as np
from verifier import *
from utils import *

class Prover:

    def __init__(self, counter_v=0):
        self.shared_key = -1
        self.verifier = Verifier(counter_v)

    def compute_key(self, lk, isAttacker=False):
        key = np.random.choice(2, lk, p=[0.5, 0.5])
        self.verifier.shared_key = key
        self.lk = lk
        if not isAttacker:
            self.shared_key = key
        return self.shared_key

    def send_welcome(self, lc):
        # no need to send u1, just accept u2
        self.c, self.n = self.verifier.get_challenge(lc)
        return self.c, self.n

    def compute_u3(self):
        if type(self.shared_key) is int and self.shared_key == -1:
            r = build_stat_response(self.lk, self.c, self.n)
        else:
            r = build_response(self.shared_key, self.c, self.n)
        return self.verifier.verify_u3(r), r
        
    def attack_observed_round(self, prev_c, prev_r, current_c, lc):
        prev_sc = sum_digits(bin_to_int(prev_c))
        if (prev_sc != 0):
            prev_st = bin_to_int(prev_r)//prev_sc
            sc = sum_digits(bin_to_int(current_c))
            st = prev_st - 2 
            #st = prev_st + 7
            r = int_to_bin(sc*st)
        else: r = int_to_bin(0)
        return r

def build_stat_response(lk, c, n):
    # replace with non-brute approach
    key = np.random.choice(2, lk, p=[0.5, 0.5])
    r = build_response(key, c, n)
    return r