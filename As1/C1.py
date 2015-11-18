#!/usr/bin/python

import random

k = 4
n = 997 # if this is prime, gcd(n, r1) will be 1
e = 3

def two_hash(a, b):
	return hash(int(str(a) + str(b)))

hash_func = two_hash
f = two_hash


class Bank(object):
	'''
	A bank with the one purpose of serving ONE
	single customer with one single withdrawal errand
	once.
	'''
	def __init__(self):
		pass

	def withdraw1(self, bs):
		self.bs = bs
		n_indexes = len(bs)
		indexes = range(n_indexes)
		random.shuffle(indexes)
		self.proof_indexes = indexes[:n_indexes / 2]
		return self.proof_indexes

	def withdraw2(self, proof, ID):
		x_ys = get_x_ys(proof, ID)
		bs = get_bs(proof, x_ys)
		for i, b in zip(self.proof_indexes, bs):
			if self.bs[i] != b:
				print "fail!"
				return False
		inv = modinv(e, n)
		sig_factors = [(self.bs[i]**inv) % n for i in xrange(2 * k) if i not in self.proof_indexes]
		sign = 1
		for factor in sig_factors:
			sign *= factor
			sign %= n
		return sign

class Alice(object):
	def __init__(self, bank, ID=13):
		self.bank = bank
		self.ID = ID
		pass

	def withdrawal(self):
		quads = get_2k_quadruples(k)
		x_ys = get_x_ys(quads, self.ID)
		bs = get_bs(quads, x_ys)
		proof_indexes_r = self.bank.withdraw1(bs)
		proofs = [quads[i] for i in proof_indexes_r]
		blind_sign = self.bank.withdraw2(proofs, self.ID)
		for [a,c,d,r] in proofs:
			r_inv = modinv(r, n)
			blind_sign = blind_sign * r_inv % n
		sign = blind_sign
		print "this is the sign:", sign

def egcd(a, b):
	if a == 0:
		return [b, 0, 1]
	else:
		gcd, y, x = egcd(b % a, a)
		return (gcd, x - (b // a) * y, y)

def modinv(a, m):
	gcd, x, y = egcd(a, m)
	if gcd != 1:
		return None
	else:
		return x % m

def get_2k_quadruples(k):
	# we make sure that no numbers are==0
	quads = [[int(random.random()*(n-1) + 1 ) for i in xrange(4)] for q in xrange(k*2)]
	return quads

def get_x_ys(quads, ID):
	x_ys = [[hash_func(a, c), hash_func((a ^ ID), d)] for [a,c,d,r] in quads]
	return x_ys

def get_bs(quads, x_ys):
	bs = [((r**e) * f(x, y)) % n for [a,c,d,r], [x,y] in zip(quads, x_ys)]
	return bs

def main():
	bank = Bank()
	alice = Alice(bank)
	alice.withdrawal()


if __name__ == '__main__':
	main()
