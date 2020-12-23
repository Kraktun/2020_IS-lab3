from prover import *
from utils import *
import time
import random
from tqdm import tqdm
import matplotlib.pyplot as plt

lc_values = [4, 8, 16, 20, 24, 28, 30, 32, 64, 128]
lk_values = [4, 8, 16, 20, 24, 28, 30, 32, 64, 128]

def alg_complexity():
	
    fig = plt.figure()
    for lc in tqdm(lc_values):
        avg_time = []
        for lk in lk_values:
            p = Prover(counter_v=0)
            p.compute_key(lk=lk, isAttacker=False)
            repetitions = 10**3
            avg = 0
            for i in range(repetitions):
                start = time.time()
                c, n = p.send_welcome(lc=lc) # generate challenge and n
                p.compute_u3() # compute r, r1 from c and n and verify that r = r1
                end = time.time()
                avg += (end-start)
            avg_time.append(avg/repetitions)
        plt.plot(lc_values, avg_time)
    plt.legend([ f"lc = {x}" for x in lc_values])
    plt.title('Algorithm complexity')
    plt.xlabel('key length')
    plt.ylabel('average elapsed time')
    plt.show(block = False)
	
def attack_as_observer():
    # ATTACK WITH OBSERVED PREVIOUS ROUND
    fig = plt.figure()
    avg_holder = []
    for lc in tqdm(lc_values):
        success_rate = []
        avg_time = []
        for lk in lk_values:
            success = 0
            repetitions = 10**3
            avg = 0
            for i in range(repetitions):
                # simulate the observed round
                counter = random.randint(0, 200)
                p = Prover(counter_v=counter)
                p.compute_key(lk=lk, isAttacker=False)
                prev_c, prev_n = p.send_welcome(lc=lc)
                result, prev_r = p.compute_u3()
				
                # simulate current round
                for j in range(0, 24):
                    c, n = p.verifier.get_challenge(lc)
				
                start = time.time()
                c, n = p.send_welcome(lc=lc)
                r = p.attack_observed_round(prev_c, prev_r, c, lc)
                result, true_r = p.verifier.verify_u3(r)
                end = time.time()
                if (result):
                    success += 1
                avg += (end-start)
            success_rate.append(success/repetitions)
            avg_time.append(avg/repetitions)
        plt.plot(lk_values, success_rate)
        avg_holder.append(avg_time)
    plt.title('Attack success rate (observer)')
    plt.legend([ f"lc = {x}" for x in lc_values])
    plt.xlabel('key length')
    plt.ylabel('success rate')
    plt.show(block = False)

    fig = plt.figure()
    for avg in avg_holder:
        plt.plot(lk_values, avg)
    plt.title('Attack complexity (observer)')
    plt.legend([ f"lc = {x}" for x in lc_values])
    plt.xlabel('key length')
    plt.ylabel('average elapsed time')
    plt.show(block = False)

def attack_brute():
    # ATTACK WITHOUT OBSERVING PREVIOUS ROUNDS
    fig = plt.figure()
    avg_holder = []
    for lc in tqdm(lc_values):
        success_rate = []
        avg_time = []
        for lk in lk_values:
            success = 0
            repetitions = 10**3
            avg = 0
            for i in range(repetitions):
                # simulate a random round
                counter = random.randint(0, 200)
                p = Prover(counter_v=counter)
                p.compute_key(lk=lk, isAttacker=True)
                start = time.time()
                c, n = p.send_welcome(lc=lc) # generate challenge and n
                result = p.compute_u3()
                end = time.time()
                if (result[0][0]):
                    success += 1
                avg += (end - start)
            success_rate.append(success/repetitions)
            avg_time.append(avg/repetitions)
        plt.plot(lk_values, success_rate)
        avg_holder.append(avg_time)
    plt.title('Attack success rate (brute)')
    plt.legend([ f"lc = {x}" for x in lc_values])
    plt.xlabel('key length')
    plt.ylabel('success rate')
    plt.show(block = False)

    fig = plt.figure()
    for avg in avg_holder:
        plt.plot(lk_values, avg)
    plt.title('Attack complexity (brute)')
    plt.legend([ f"lc = {x}" for x in lc_values])
    plt.xlabel('key length')
    plt.ylabel('average elapsed time')
    plt.show(block = False)
	
if __name__ == "__main__": 
    alg_complexity()
    #attack_as_observer()
    #attack_brute()
    plt.show()
