#!/usr/bin/env python

# @file rfc.py
# @author sb

from __future__ import print_function
from fileinput import input as inp
from urllib2 import urlopen

# todo handling side
# 1. First write a program for getting the text file from the required location

# globals section
RFC_REF = 'https://www.rfc-editor.org/rfc/rfc-ref.txt'
RFC_LOCAL_REF = './rfc-ref.txt'

# @function get_rfc_index
# @details function to download the text file from the specified location. the
# file that will be downloaded is actually the index file containing
# information about the RFCs that have come out
def get_rfc_index(url_dwnl):
	response = urlopen(RFC_REF)
	data = response.read()
	lines = str(data).split('\n')

# @function main
# @details function that performs the choreographing and calls the necessary
# functions based on the requirements
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
