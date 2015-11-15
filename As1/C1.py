#!/usr/bin/python

import random

k = 2
n = 100



def two_hash(a, b):
	return hash(int(str(a) + str(b)))

hash_func = two_hash
f = two_hash


class Bank(object):
	def __init__(self):
		pass

	def whitdraw1(self, bs):
		self.bs = bs
		n_indexes = len(bs)
		indexes = range(n_indexes)
		random.shuffle(indexes)
		self.proof_indexes = indexes[:n_indexes / 2]
		self.not_r = indexes[n_indexes / 2:]
		return self.proof_indexes

	def whitdraw2(self, proof):
		x_ys = get_x_ys(proof)
		bs = get_bs(proof, x_ys)
		for i, b in zip(self.proof_indexes, bs):
			if self.bs[i] != b:
				print "fail!"
				return False
		print "All is ok"
		#self.not_r

class Alice(object):
	def __init__(self, bank):
		self.bank = bank
		pass

	def whitdrawal(self):
		quads = get_2k_quadruples(k)
		x_ys = get_x_ys(quads)
		bs = get_bs(quads, x_ys)
		proof_indexes_r = self.bank.whitdraw1(bs)
		proofs = [quads[i] for i in proof_indexes_r]
		self.bank.whitdraw2(proofs)

def get_2k_quadruples(k=10):
	quads = [[int(random.random()*n) for i in xrange(4)] for q in xrange(k*2)]
	return quads

def get_x_ys(quads, ID=2):
	x_ys = [[hash_func(a, c), hash_func((a ^ ID), d)] for [a,c,d,r] in quads]
	return x_ys

def get_bs(quads, x_ys):
	bs = [((r**3) * f(x, y)) % n for [a,c,d,r], [x,y] in zip(quads, x_ys)]
	return bs

def main():
	bank = Bank()
	a = Alice(bank)
	a.whitdrawal()


if __name__ == '__main__':
	main()