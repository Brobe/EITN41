#!/usr/bin/python

import random
import sys
import numpy as np

n = 4
# m less or eq N/n. => insecure

#we let alice be labeled 0

class Mix():
	def __init__(self, N, b, m):
		if b < n:
			print "failed as b < n"
			sys.exit(1)
		if m > float(N) / n:
			print "failed as m > N/n"
			sys.exit(1)
		self.alice = 0
		self.users_except_alice = range(1, N)
		self.alice_partners = self.users_except_alice[:m]
		self.non_alice_partners = self.users_except_alice[m:]
		self.N = N
		self.b = b
		self.m = m

	def alice_batch(self):
		random.shuffle(self.users_except_alice)
		senders = self.users_except_alice[:self.b-1] + [self.alice]
		receivers = random.sample(self.non_alice_partners, n-1)
		receivers.append(random.choice(self.alice_partners))
		return senders, set(receivers)

def learn_rec_set(disjoints, new_receivers):
	for r in disjoints:
		if not r.isdisjoint(new_receivers):
			break
	else:
		disjoints.append(new_receivers)

def exclude_rec_set(disjoints, new_receivers):
	non_disjunct = [(i, rj) for i, rj in enumerate(disjoints) if not rj.isdisjoint(new_receivers)]
	if len(non_disjunct) == 1:
		i = non_disjunct[0][0]
		disjoints[i] = non_disjunct[0][1] & new_receivers

def is_singled_out(disjoints):
	for r in disjoints:
		if len(r) > 1:
			return False
	else:
		return True

def simulate_attack(N, b, m):
	mix = Mix(N, b, m)
	#learning phase!
	disjoint = list()
	n_learn_batches = 0
	n_exc_batches = 0
	#learning phase
	while(len(disjoint) < m):
		n_learn_batches += 1
		senders, receivers = mix.alice_batch()
		learn_rec_set(disjoint, receivers)
	#excluding phase
	while(not is_singled_out(disjoint)):
		n_exc_batches += 1
		senders, receivers = mix.alice_batch()
		exclude_rec_set(disjoint, receivers)
	disjoint.sort()
	return n_learn_batches + n_exc_batches
	#print "WE FOUND THESE PARTNERS:", " ".join([str(list(s)[0]) for s in disjoint])
	#print "n_learn_bathces", n_learn_batches
	#print "n_exc_bathces", n_exc_batches



def plot(Ns, ms, complexities):
	from mpl_toolkits.mplot3d import Axes3D
	from matplotlib import cm
	from matplotlib.ticker import LinearLocator, FormatStrFormatter
	import matplotlib.pyplot as plt


	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	X = np.array(Ns)
	Y = np.array(complexities)
	Z = np.array(ms)
	ax.bar(X, Y, zs=Z, zdir='y')
	ax.set_xlabel('N')
	ax.set_ylabel('m')
	ax.set_zlabel('complexity')
	plt.show()

def main():
	# N = total user base
	# m = communication partners
	b = n # senders in each batch
	NMIN, NMAX = 10, 50
	simuls = 10
	Ns = []
	ms = []
	complexities = []

	for N_i in xrange(NMIN, NMAX + 1):
		for m_i in xrange(1, N_i/n):
			Ns.append(N_i)
			ms.append(m_i)
			average_comp = np.mean([simulate_attack(N_i, b, m_i) for _ in xrange(simuls)])
			complexities.append(average_comp)
	for l in [("n", N_i, "m", m_i, "c", c_i) for N_i, m_i, c_i in zip(Ns, ms, complexities)]:
		print l
	plot(Ns, ms, complexities)



if __name__ == '__main__':
	main()