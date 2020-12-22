from prover import *
from utils import *
from timeit import default_timer as timer
import numpy as np
import matplotlib.pyplot as plt

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

def time_tb():
    l_c = np.ceil(np.logspace(1.0, 6.0, num=20, base=2))
    l_k = l_c
    results_lk = []
    p = Prover(counter_v=0)
    l_ci = 10
    for l_ki in l_k:
        start = timer()
        # multiple runs to get a better estimate
        for z in range(300):
            p.compute_key(lk=int(l_ki), isAttacker=False)
            c, n = p.send_welcome(lc=int(l_ci))
            res = p.send_encrypted()
        end = timer()
        results_lk.append(end - start)
    print(results_lk)

    results_lc = []
    p = Prover(counter_v=0)
    l_ki = 10
    for l_ci in l_c:
        start = timer()
        for z in range(300):
            p.compute_key(lk=int(l_ki), isAttacker=False)
            c, n = p.send_welcome(lc=int(l_ci))
            res = p.send_encrypted()
        end = timer()
        results_lc.append(end - start)
    print(results_lc)

    fig = plt.figure()
    ax = plt.subplot(111)
    plt.plot(l_k, results_lk)
    plt.title('Algorithm complexity')
    plt.xlabel('lk')
    plt.ylabel('time')
    plt.show(block = False)

    fig = plt.figure()
    ax = plt.subplot(111)
    plt.plot(l_c, results_lc)
    plt.title('Algorithm complexity')
    plt.xlabel('lc')
    plt.ylabel('time')
    plt.show(block = False)

if __name__ == "__main__": 
    #main()
    time_tb()
    plt.show()
