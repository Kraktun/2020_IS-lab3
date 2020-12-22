from prover import *
from utils import *

def main():
    lc = 10
    lk = 10
    p = Prover(counter_v=0)
    p.compute_key(lk=lk, isAttacker=False)
    print("shared key: " + array_to_string(int_to_bin(p.shared_key))) # you can print directly the number if you prefer
    for i in range(10):
        c, n = p.send_welcome(lc=lc)
        print("Round: " + str(n))
        print("c: " + array_to_string(c))
        res = p.send_encrypted()
        print("result: " + str(res))
        print("#######################")

if __name__ == "__main__": 
    main()
