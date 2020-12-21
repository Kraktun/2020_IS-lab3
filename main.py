from prover import *
from utils import *

def main():
    lc = 10
    lk = 10
    p = Prover(counter_v=0)
    p.compute_key(lk=lk, isAttacker=False)
    print("shared key: " + array_to_string(p.shared_key))
    for i in range(10):
        c, n = p.send_welcome(lc=lc)
        print("c: " + array_to_string(c) + "\nn: " + str(n))
        res = p.send_encrypted()
        print("result: " + str(res))

if __name__ == "__main__": 
    main()
