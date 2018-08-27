#!/usr/bin/env python

# @file rfc.py
# @author sb

from __future__ import print_function
from fileinput import input as inp
from urllib2 import urlopen
from fileinput import input as inp

# todo handling side
# 1. First write a program for getting the text file from the required location

# globals section
RFC_REF = 'https://www.rfc-editor.org/rfc/rfc-ref.txt'
RFC_LOCAL_REF = './rfc-ref.txt'

# @class Rfc
# @details class to contain the name of the RFC, the nuber of the same and the
# title of the RFC
class Rfc:
	def __init__(self, rfc_name, rfc_num, rfc_title):
		self.name = rfc_name
		self.num = rfc_num
		self.title = rfc_title

	# set variable functions
	def set_name(self, rfc_name):
		self.name = rfc_name
	def set_num(self, rfc_num):
		self.num = rfc_num
	def set_title(self, rfc_title):
		self.title = rfc_title

	# get data functions
	def get_name(self):
		return self.name
	def get_num(self):
		return self.num
	def get_title(self):
		return self.title

# @function get_rfc_index
# @details function to download the text file from the specified location. the
# file that will be downloaded is actually the index file containing
# information about the RFCs that have come out
def get_rfc_index(url_dwnl, filepath):
	response = urlopen(url_dwnl)
	data = response.read()
	lines = str(data).split('\n')

	# always rewrite the file - since the data content should never be
	# appended
	f = open(filepath, 'w')
	for line in lines:
		f.write(line + '\n')
	f.close()

# @function parse_rfc_ref
# @details function to parse the contents of the file as mentioned as the value
# of RFC_LOCAL_REF. After parsing the data has to be put into a map or
# container of some kind
def parse_rfc_ref(filepath):
	for line in inp([filepath]):
		line = line.strip()
		print(line)

		# create the class before parsing and pushing in the data

# @function main
# @details function that performs the choreographing and calls the necessary
# functions based on the requirements
def main():
	# get the reference file downloaded
	get_rfc_index(RFC_REF, RFC_LOCAL_REF)

	# now call the function which will be reading through the file
	parse_rfc_ref(RFC_LOCAL_REF)

	#for line in inp(['./details_rfc']):
		#if 'RFC' in line.strip():
			#mkey_list = line.strip().split('|')
			#print(len(mkey_list))
			#for i in xrange(0, len(mkey_list)):
				#if i == 0:
					## this is the name of the RFC
					#print(mkey_list[i], end = '\t')
				#elif i == len(mkey_list) -1:
					# this is the one with the extra amount
					# of data
					#last_data = (mkey_list[i].strip())

					## now get the title of the RFC
					#print(last_data[last_data.index('"') +
						#1 : last_data.rfind('",')])
			#break

if __name__ == '__main__':
	main()
