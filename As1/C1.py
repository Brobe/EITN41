#!/usr/bin/python

import random
import hashlib

k = 20
p = 492876863
q = 512927377
n = p * q # if this is prime, gcd(n, r1) will be 1
e = 5

def two_hash(a, b):
	dig = hashlib.sha256(str(a) + str(b)).hexdigest()
	return int(dig, 16)

h = two_hash
f = two_hash

class Bank(object):
	'''
	A bank with the one purpose of serving ONE
	single customer with one single withdrawal errand
	once.
	'''
	def __init__(self):
		self.d = None

	def withdraw1(self, bs):
		self.bs = bs
		n_indices = len(bs)
		indices = range(n_indices)
		random.shuffle(indices)
		self.proof_indices = indices[:n_indices / 2]
		return self.proof_indices

	def withdraw2(self, proof, ID):
		x_ys = get_x_ys(proof, ID)
		bs = get_bs(proof, x_ys)
		for i, b in zip(self.proof_indices, bs):
			if self.bs[i] != b:
				print "fail!"
				return False
		inv = modinv(e, (p - 1) * (q - 1))
		self.d = inv
		print "INV", inv
		sig_factors = [pow(self.bs[i], inv, n) for i in xrange(2 * k) if i not in self.proof_indices]
		sign = 1
		for factor in sig_factors:
			sign *= factor
			sign %= n
		return sign

class Alice(object):
	def __init__(self, bank, ID=13):
		self.bank = bank
		self.ID = ID
		self.bs = None
		pass

	def withdrawal(self):
		self.quads = get_2k_quadruples(k)
		x_ys = get_x_ys(self.quads, self.ID)
		self.bs = get_bs(self.quads, x_ys)
		proof_indices_r = self.bank.withdraw1(self.bs)
		proofs = [self.quads[i] for i in proof_indices_r]
		blind_sign = self.bank.withdraw2(proofs, self.ID)
		for [a,c,d,r] in proofs:
			r_inv = modinv(r, n)
			blind_sign = blind_sign * r_inv % n
		sign = blind_sign
		print "this is the sign:", sign
		return sign

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
	quads = []
	for _ in xrange(k*2):
		acdr = [int(random.randint(0, n-1)) for _ in xrange(3)]
		r = random.randint(0, n-1)
		while egcd(r, n)[0] != 1:
			r = random.randint(0, n-1)
		acdr.append(r)
		quads.append(acdr)
	return quads

def get_x_ys(quads, ID):
	x_ys = [[h(a, c), h((a ^ ID), d)] for [a,c,d,r] in quads]
	return x_ys

def get_bs(quads, x_ys):
	bs = [(pow(r, e) * f(x, y)) % n for [a,c,d,r], [x,y] in zip(quads, x_ys)]
	return bs

def test(B, bank, ID, indices, S):
#just making sure the algo is correct
        real_S = 1
        for i, (ai, ci, di, ri) in enumerate(B):
            if i not in indices:
                real_S = (real_S * pow(f(h(ai, ci), h(ai ^ ID, di)), bank.d, n)) % n

        return S, real_S

def main():
	bank = Bank()
	alice = Alice(bank)
	sign = alice.withdrawal()
	print test(alice.quads, bank, alice.ID, bank.proof_indices, sign)
	print pow(2, e*bank.d, n)

if __name__ == '__main__':
	main()
