#!/usr/bin/python
from collections import defaultdict
import random
import hashlib

n_bins = 1<<5 # 2**5
hash_mask = n_bins - 1
k = 6

possible_start_vals = 100
start_val = int(random.random() * possible_start_vals)

def coin_hash(x):
	# we do this in order to use the hash_mask, but we want a reliable
	# hash func, we don't trust hash
	dig = hashlib.sha224(str(x)).hexdigest()
	return hash(dig) & hash_mask

def main():
	bins = defaultdict(list)
	coins = []
	#we use a random starting value
	start_val = int(random.random() * possible_start_vals)
	print "start val was: ", start_val
	for x in xrange(start_val, start_val + k * n_bins):
		#create the hash
		h_val = coin_hash(x)
		#add the hash to the proper bin
		bins[h_val].append(x)

		if len(bins[h_val]) == k:
			#if we're here, we have a coin, woo!!
			coins.append(bins[h_val])
			#let's empty the bin
			bins[h_val] = []
	print_coins(coins)

def print_coins(coins):
	for i, coin in enumerate(coins):
		print i, ":", coin

if __name__ == '__main__':
	main()
