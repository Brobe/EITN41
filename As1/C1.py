#!/usr/bin/python

import random

MAX_RAND = 10**2
k = 2
n = 10

hash_func = hash
f = hash
class Bank(object):
	def __init__(self):
		pass

	def whitdrawal(args):
		pass

class Alice(object):
	def __init__(self):
		pass
	def whitdrawal(args):
		pass

def get_2k_quadruples(k=10):
	quads = [[int(random.random()*MAX_RAND) for i in xrange(4)] for q in xrange(k*2)]
	return quads

def get_x_ys(quads, ID=2):
	x_ys = [[hash_func(int(str(a) + str(c))), hash_func(int(str(a ^ ID) + str(d)))] for [a,c,d,r] in quads]
	return x_ys

def get_bs(quads, x_ys):
	bs = [((r**3) * f(int(str(x)+str(y)))) % n for [a,c,d,r], [x,y] in zip(quads, x_ys)]
	return bs

def main():
	quads = get_2k_quadruples(k)
	x_ys = get_x_ys(quads)
	bs = get_bs(quads, x_ys)
	print quads
	print x_ys
	print bs

if __name__ == '__main__':
	main()