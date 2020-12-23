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
            start = time.time()
            for i in range(repetitions):
                c, n = p.send_welcome(lc=lc) # generate challenge and n
                p.compute_u3() # compute r, r1 from c and n and verify that r = r1
            end = time.time()
            avg = (end-start)/repetitions
            avg_time.append(avg)
        plt.plot(lc_values, avg_time)
    plt.legend([ f"lc = {x}" for x in lc_values])
    plt.title('Algorithm complexity')
    plt.xlabel('key length')
    plt.ylabel('average elapsed time')
    plt.show(block = False)
	
def attack_observer():
	# ATTACK WITH OBSERVED PREVIOUS ROUND
	lc_values = [4, 8, 16, 20, 24, 28, 30, 32, 64, 128]
	lk_values = [4, 8, 16, 20, 24, 28, 30, 32, 64, 128]
	for c in lc_values:
		lc = c
		success_rate = []
		for k in tqdm(lk_values):
			lk = k
			success = 0
			for i in range(10**3):
				# simulate the observed round
				counter = random.randint(0, 200)
				p = Prover(counter_v=counter)
				p.compute_key(lk=lk, isAttacker=False)
				prev_c, prev_n = p.send_welcome(lc=lc)
				result, prev_r = p.compute_u3()
				
				# simulate current round
				for i in range(0, 24):
					p.verifier.get_challenge(lc)
					
				c, n = p.send_welcome(lc=lc)
				r = p.attack_observed_round(prev_c, prev_r, c, lc)
				result, true_r = p.verifier.verify_u3(r)
				if (result):
					success += 1
			success_rate.append(success/10**3)
		plt.plot(lk_values, success_rate)
	plt.xlabel('key length')
	plt.ylabel('success rate')
	plt.legend(lc_values)
	plt.show()
	
def attack_brute():
	# ATTACK WITH OBSERVED PREVIOUS ROUND
	lc_values = [4, 8, 16, 20, 24, 28, 30, 32, 64, 128]
	lk_values = [4, 8, 16, 20, 24, 28, 30, 32, 64, 128]
	for c in lc_values:
		lc = c
		avg_time = []
		for k in tqdm(lk_values):
			lk = k
			avg = 0
			for i in range(10**3):
				# simulate the observed round
				counter = random.randint(0, 200)
				p = Prover(counter_v=counter)
				p.compute_key(lk=lk, isAttacker=False)
				prev_c, prev_n = p.send_welcome(lc=lc)
				result, prev_r = p.compute_u3()
				
				# simulate current round
				for i in range(0, 24):
					p.verifier.get_challenge(lc)
				start = time.time()
				c, n = p.send_welcome(lc=lc)
				r = p.attack_observed_round(prev_c, prev_r, c, lc)
				result, true_r = p.verifier.verify_u3(r)
				end = time.time()
				avg = avg + (end-start)
			avg_time.append(avg/10**3)
		plt.plot(lk_values, avg_time)
	plt.xlabel('key length')
	plt.ylabel('average elapsed time')
	plt.legend(lc_values)
	plt.show()

if __name__ == "__main__": 
    alg_complexity()
    plt.show()
