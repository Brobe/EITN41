#!/usr/bin/python

import hashlib
import random
import sys
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt


FAILURE = -1

class Enemy(object):
	def __init__(self, hash_func):
		self.hash_f = hash_func

	def break_binding(self, original, v):
		'''
		Find k such that hash(!v, k) == original
		Returns the number of itterations needed
		'''
		k = 0
		for k in xrange((1 << 16) + 1):
			if original == self.hash_f(1 ^ v, k):
				break
		else:
			k = FAILURE
		return k

class Hash(object):
	def __init__(self, X):
		self.X = X

	def hash_f(self, v, k):
		dig = hashlib.sha256(str(v) + str(k)).hexdigest()
		return int(dig, 16) & (1 << self.X) - 1

def rand_16():
	mask_16 = (1<<16) - 1
	return random.randint(0, sys.maxint) & mask_16


def simulate_break(X, v, n_itter):
	'''
	Returns:
		cost, success_rate
	 		cost: the average number of tries for the successes,
	 		success_rate: The successrate
	'''
	hash_func = Hash(X).hash_f
	enemy = Enemy(hash_func)
	cost = []
	n_successes = 0.0
	for _ in xrange(n_itter):
		k = rand_16()
		original_ballot = hash_func(v, k)
		n_itterations = enemy.break_binding(original_ballot, v)
		if n_itterations != FAILURE:
			n_successes += 1.0
			cost.append(n_itterations)

	avg_cost = np.array(cost).mean() if cost else 0.0 
	return avg_cost, n_successes/n_itter

def main():
	random.seed(1)
	MIN_X, MAX_X = 12, 24
	n_itter = 10
	XS = range(MIN_X, MAX_X + 1)
	binding_break_cost = []
	success_rates = []
	for X in XS:
		v = (X & 0x1)
		cost, success_rate = simulate_break(X, v, n_itter)
		binding_break_cost.append(cost)
		success_rates.append(success_rate)
	print "displaying break binding cost plot"
	plot(XS, binding_break_cost, title ="break binding cost (0 if no success achieved)",
		X_label="bits", Y_label="mean nbr of itterations to achieve success (0 if failure)")

	print "displaying break binding success rate plot"
	plot(XS, success_rates, title ="success rate",
		X_label="bits", Y_label="success rate")

def plot(X, Y, title="plot", X_label="X", Y_label="Y"):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	X = np.array(X)
	Y = np.array(Y)
	ax.bar(X, Y)
	plt.title(title)
	ax.set_xlabel(X_label)
	ax.set_ylabel(Y_label)
	plt.show()


if __name__ == '__main__':
	#print "hash(john) = ", Hash(16).hash_f("john2","NEJ")
	main()