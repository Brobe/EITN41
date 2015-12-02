#!/usr/bin/python

import hashlib
import random
import sys
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

K_SIZE = 16

class SteveTheEnemy(object):
	'''
	Steve, the misguided genius who wants to
	break your schemes and read your votes.
	'''
	def __init__(self, hash_func):
		self.hash = hash_func
		self.hash_to_vote = defaultdict(lambda :defaultdict(int))
		for k in xrange((1 << K_SIZE)):
			zero_hash = self.hash(0, k)
			one_hash = self.hash(1, k)
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
		find out if we can find k0 and k1 such that
		h(0, k0) == h(1, k1) == ballot.
		If so, we cannot break the concealing property
		Returns whether or not we can break the concealing property
		'''
		zero_count = self.hash_to_vote[ballot][0]
		one_count = self.hash_to_vote[ballot][1]
		return not (zero_count > 0 and one_count > 0)


class XBitHash(object):
	def __init__(self, X):
		self.X = X

	def hash(self, v, k):
		dig = hashlib.sha256(str(v) + str(k)).hexdigest()
		return int(dig, 16) & (1 << self.X) - 1


def simulate_break(X, v, n_itter):
	'''
	Returns:
		binding_break_probability, concealing_break_probability
	'''
	hash_func = XBitHash(X).hash
	enemy = SteveTheEnemy(hash_func)
	n_binding_breaks = 0.0
	n_concealing_breaks = 0.0
	for _ in xrange(n_itter):
		k = random.getrandbits(K_SIZE)
		original_ballot = hash_func(v, k)
		binding_broken = enemy.binding_breakable(original_ballot, v)
		concealing_broken = enemy.concealing_breakable(original_ballot)
		n_binding_breaks += binding_broken
		n_concealing_breaks += concealing_broken

	return n_binding_breaks/n_itter, n_concealing_breaks/n_itter

def plot1(XS, probability, Y_label="probability", title="probability"):
	plt.plot(XS, probability, linewidth=2.0)
	plt.xlabel('X, number of bits in hash outputs')
	plt.ylabel(Y_label)
	plt.legend([Y_label], loc='upper left')
	plt.title(title)
	plt.show()

def plot2(XS, binding_break_rates, concealing_break_rates, title="probability"):
	plt.plot(XS, binding_break_rates, linewidth=2.0)
	plt.plot(XS, concealing_break_rates, linewidth=2.0)
	plt.xlabel('X, number of bits in hash outputs')
	plt.ylabel('probability')
	plt.legend(["probability of\nbreaking binding",
		"probability of\nbreaking concealing"], loc='upper left')
	plt.title(title)
	plt.show()

def main():
	random.seed(1)
	MIN_X, MAX_X = 5, 25
	n_itter = 1000
	XS = range(MIN_X, MAX_X + 1)
	binding_break_rates = []
	concealing_break_rates = []
	for X in XS:
		v = (X & 0x1)
		binding_break_rate, concealing_break_rate = simulate_break(X, v, n_itter)
		binding_break_rates.append(binding_break_rate)
		concealing_break_rates.append(concealing_break_rate)

	plot1(XS, binding_break_rates, Y_label=
		"probability of\nbreaking binding",
		title="probability of breaking binding")
	plot1(XS, concealing_break_rates, Y_label=
		"probability of\nbreaking concealing",
		title="probability of breaking concealing")
	plot2(XS, binding_break_rates, concealing_break_rates,
		title="probability rates")

if __name__ == '__main__':
	main()