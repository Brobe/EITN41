#!/usr/bin/python

import hashlib
import random
import sys
import numpy as np
from collections import defaultdict

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt


FAILURE = -1

class Enemy(object):
	def __init__(self, hash_func):
		self.hash_f = hash_func
		self.hash_to_vote = defaultdict(lambda :defaultdict(int))
		for k in xrange((1 << 16)):
			zero_hash = self.hash_f(0, k)
			one_hash = self.hash_f(1, k)
			self.hash_to_vote[zero_hash][0] += 1
			self.hash_to_vote[one_hash][1] += 1

	def binding_breakable(self, ballot, v):
		'''
		Find k such that hash(!v, k) == ballot
		Returns whether it is possible or not
		'''
		return self.hash_to_vote[ballot][1 ^ v] > 0

	def concealing_breakable(self, ballot):
		'''
		Find out if it is possible to single out the hash
		so that it only votes os a special kind can generate
		the ballot
		'''
		zero_count = self.hash_to_vote[ballot][0]
		one_count = self.hash_to_vote[ballot][1]
		return not (zero_count > 0 and one_count > 0)

class Hash(object):
	def __init__(self, X):
		self.X = X

	def hash_f(self, v, k):
		dig = hashlib.sha256(str(v) + str(k)).hexdigest()
		return int(dig, 16) & (1 << self.X) - 1

def rand_16():
	mask_16 = (1<<16) - 1
	return random.randint(0, sys.maxint) & mask_16

def probability(zero_count, one_count):
	'''
	Return the probability of guessing correctly
	'''
	if zero_count > 0 and one_count > 0:
		return 0
	else:
		return 1


def simulate_break(X, v, n_itter):
	'''
	Returns:
		cost, success_rate
	 		cost: the average number of tries for the successes,
	 		success_rate: The successrate
	'''
	hash_func = Hash(X).hash_f
	enemy = Enemy(hash_func)
	n_binding_breaks = 0.0
	n_concealing_breaks = 0.0
	for _ in xrange(n_itter):
		k = rand_16()
		original_ballot = hash_func(v, k)
		binding_broken = enemy.binding_breakable(original_ballot, v)
		concealing_broken = enemy.concealing_breakable(original_ballot)
		n_binding_breaks += binding_broken
		n_concealing_breaks += concealing_broken

	print "n_binding_breaks/n_itter", n_binding_breaks/n_itter, "n_binding_breaks",\
		n_binding_breaks, "n_itter", n_itter

	print "n_concealing_breaks/n_itter", n_concealing_breaks/n_itter, "n_concealing_breaks",\
		n_concealing_breaks, "n_itter", n_itter
	return n_binding_breaks/n_itter, n_concealing_breaks/n_itter

def main():
	random.seed(1)
	MIN_X, MAX_X = 5, 25
	n_itter = 1000
	XS = range(MIN_X, MAX_X + 1)
	binding_break_rates = []
	concealing_break_rates = []
	for X in XS:
		print "X =", X
		v = (X & 0x1)
		binding_break_rate, de_concealing_rate = simulate_break(X, v, n_itter)
		binding_break_rates.append(binding_break_rate)
		concealing_break_rates.append(de_concealing_rate)

	print "displaying break binding success rate plot"
	#plot(XS, binding_break_rates, title ="success rate",
	#	X_label="bits", Y_label="success rate")

	print "displaying break concealing success rate plot"
	#plot(XS, concealing_break_rates, title ="de-success probability rate",
	#	X_label="bits", Y_label="success rate")

	plot2(XS, binding_break_rates, concealing_break_rates, title="break rates")

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

def plot2(XS, binding_break_rates, concealing_break_rates, title="break rates"):
	plt.plot(XS, binding_break_rates)
	plt.plot(XS, concealing_break_rates)
	plt.xlabel('X, number of bits in hash outputs')
	plt.ylabel('probability')
	plt.legend(['binding_break_rates', 'concealing_break_rates'], loc='upper left')
	plt.title(title)
	plt.show()


if __name__ == '__main__':
	#print "hash(john) = ", Hash(16).hash_f("john2","NEJ")
	main()