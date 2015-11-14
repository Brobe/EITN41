#!/usr/bin/python

import sys
import random

def double(card_nbrs):
	check_sum = card_nbrs[-1]
	doubles = [v*2 if i%2 == 0 else v for i, v in enumerate(card_nbrs[-2::-1])]
	doubles = [(v % 10 + v/10) if v>=10 else v for v in doubles]
	card_sum = sum(doubles)
	if card_sum * 9 % 10 == check_sum:
		print "valid!!"
		return True
	else:
		print "you haz failed!"
		return False


def make_nbr():
	#make 16 digits
	card_nbr = [int(random.random()*10) for d in xrange(15)]
	doubles = [v*2 if i%2 == 0 else v for i, v in enumerate(card_nbr[::-1])]
	doubles = [(v % 10 + v/10) if v>=10 else v for v in doubles]
	card_sum = sum(doubles)
	check_sum = card_sum * 9 % 10
	card_nbr += [check_sum]
	print "trying:", card_nbr
	double(card_nbr)
	return card_nbr

def main(argv):
	if len(argv) >= 1 and argv[0] == "gen":
		make_nbr()
		return
	if len(argv) >= 1:
		card_nbr_str = "".join(argv)
	else:
		card_nbr_str = raw_input("give us your card nbr!: ")
	card_nbr_str = card_nbr_str.replace(" ", "")
	card_nbr = [int(v) for v in card_nbr_str]
	double(card_nbr)

if __name__ == '__main__':
	

	main(sys.argv[1:])