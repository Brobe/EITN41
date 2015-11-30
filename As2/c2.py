#!/usr/bin/python

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import random
import sys
import numpy as np

n = 3
class Mix():
	def __init__(self, N, b, m):
		assert b >= n, "b: %r is less than n: %r" % (b, n)
		assert m <= float(N) / n,\
			"m: %r is larger than N/n: %r" % (m, float(N) / n)
		self.alice = 0
		self.users_except_alice = range(1, N)
		self.all_users = range(0, N)
		self.alice_partners = self.users_except_alice[:m]
		self.non_alice_partners = self.users_except_alice[m:] + [self.alice]
		self.b = b

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
	non_disjunct = [(i, rj) for i, rj in 
		enumerate(disjoints) if not rj.isdisjoint(new_receivers)]
	if len(non_disjunct) == 1:
		i = non_disjunct[0][0]
		disjoints[i] = non_disjunct[0][1] & new_receivers

def attack_has_succeeded(disjoints):
	for r in disjoints:
		if len(r) > 1:
			return False
	else:
		return True

def simulate_attack(N, b, m):
	'''
	Returns the number of batches read before
	the attack succeeded.
	'''
	mix = Mix(N, b, m)
	disjoint = list()
	n_learn_batches = 0
	n_exc_batches = 0
	#learning phase
	while len(disjoint) < m:
		n_learn_batches += 1
		senders, receivers = mix.alice_batch()
		print disjoint, receivers
                learn_rec_set(disjoint, receivers)

	print "learning done"
        #excluding phase
	while not attack_has_succeeded(disjoint):
		n_exc_batches += 1
		senders, receivers = mix.alice_batch()
		print disjoint, receivers
		exclude_rec_set(disjoint, receivers)
	disjoint.sort()
	return n_learn_batches + n_exc_batches

def main():
	b = n # senders in each batch
	NMIN, NMAX = 1, 20
	mMIN = 3
	simuls = 10
	Ns = []
	ms = []
	n_batches = []

	for N_i in xrange(NMIN, NMAX + 1):
		for m_i in xrange(mMIN, N_i / n + 1):
			print "N", N_i, "m", m_i
			Ns.append(N_i)
			ms.append(m_i)
			average_comp = np.mean([simulate_attack(N_i, b, m_i) for _ in xrange(simuls)])
			n_batches.append(average_comp)
	for l in [("n", N_i, "m", m_i, "c", c_i) for N_i, m_i, c_i in zip(Ns, ms, n_batches)]:
		print l
	plot(Ns, ms, n_batches)

def plot(Ns, ms, n_batches):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	X = np.array(Ns)
	Y = np.array(n_batches)
	Z = np.array(ms)
	ax.bar(X, Y, zs=Z, zdir='y')
	ax.set_xlabel('N')
	ax.set_ylabel('m')
	ax.set_zlabel('n_batches')
	plt.show()

if __name__ == '__main__':
	main()
