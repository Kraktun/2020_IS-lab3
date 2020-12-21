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
        if not isAttacker:
            self.shared_key = key
        return self.shared_key

    def send_welcome(self, lc):
        # no need to send u1, just accept u2
        self.c, self.n = self.verifier.get_challenge(lc)
        return self.c, self.n

    def send_encrypted(self):
        r = build_response(self.shared_key, self.c, self.n)
        return self.verifier.verify_encryption(r)
