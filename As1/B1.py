#!/usr/bin/python
# this script may be used in two different ways:
# $	./B1.py gen 	-> create a random card number 
# $	./B1.py check 	-> check if a card number is valid
#
# you may also provide a card number directly as an argument
# when you use 'check', like so:
# $ ./B1.py check 12345678
# the numbers may also be split up
# $ ./B1.py check 1234 5678 9012 3456

import sys
import random

commands = ['gen', 'check']

def card_nbr_check(card_nbr):
	'''
	Verifies if the vard_nbr
	'''
	check_sum = card_nbr[-1]
	doubles = [v*2 if i%2 == 0 else v for i, v in enumerate(card_nbr[-2::-1])]
	doubles = [(v % 10 + v/10) if v>=10 else v for v in doubles]
	card_sum = sum(doubles)
	return card_sum * 9 % 10 == check_sum

def make_card_nbr():
	'''
	Create a 16 digits valid card number
	'''
	card_nbr = [int(random.random()*10) for d in xrange(15)]
	second_doubles_pre = [v*2 if i%2 == 0 else v for i, v in enumerate(card_nbr[::-1])]
	second_doubles = [(v % 10 + v/10) if v>=10 else v for v in second_doubles_pre]
	digit_sum = sum(second_doubles)
	check_sum = digit_sum * 9 % 10
	card_nbr.append(check_sum)
	is_ok = card_nbr_check(card_nbr)
	if not is_ok:
		print "we failed, something is wrong with the implementation."
		sys.exit(1)
	return card_nbr

def main(argv):
	is_gen = "gen" in argv
	is_check = "check" in argv
	argv = filter(lambda arg: arg not in commands, argv)
	if is_gen:
		nbr = make_card_nbr()
		print "".join([str(d) for d in nbr])
	elif is_check:
		card_nbr_str = None
		if len(argv) >= 1:
			card_nbr_str = "".join(argv)
		else:
			card_nbr_str = raw_input("give us your card nbr!: ")
		card_nbr_str = card_nbr_str.replace(" ", "")
		card_nbr = [int(v) for v in card_nbr_str]
		if card_nbr_check(card_nbr):
			print "number IS valid!"
		else:
			print "number is NOT valid"
	else:
		print "please specify one of the valid commands:", commands

if __name__ == '__main__':
	main(sys.argv[1:])