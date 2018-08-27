#!/usr/bin/env python

# @file rfc.py
# @author sb

from __future__ import print_function
from fileinput import input as inp

def main():
	for line in inp(['./details_rfc']):
		if 'RFC' in line.strip():
			mkey_list = line.strip().split('|')
			print(len(mkey_list))
			for i in xrange(0, len(mkey_list)):
				if i == 0:
					# this is the name of the RFC
					print(mkey_list[i], end = '\t')
				elif i == len(mkey_list) -1:
					# this is the one with the extra amount
					# of data
					last_data = (mkey_list[i].strip())

					# now get the title of the RFC
					print(last_data[last_data.index('"') +
						1 : last_data.rfind('",')])
			break

if __name__ == '__main__':
	main()
