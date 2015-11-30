#!/usr/bin/python

import hashlib


class Hash(object):
	mask_16 = (1<<2) - 1
	def __init__(self, X):
		self.X = X

	def hash(self, v, k):
		dig = hashlib.sha256(str(v) + str(k)).hexdigest()
		return int(dig, 16) & Hash.mask_16



if __name__ == '__main__':
	k = "I am sooo random"
	v = 1
	X = 11
	print Hash(X).hash(v, k)
