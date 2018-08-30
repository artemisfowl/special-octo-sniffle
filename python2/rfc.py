#!/usr/bin/env python

# @file rfc.py
# @author sb

from __future__ import print_function
from fileinput import input as inp
from urllib2 import urlopen
from fileinput import input as inp
from os import path, makedirs, system
from glob import glob

# todo handling side
# 1. First write a program for getting the text file from the required location

# globals section
RFC_REF = 'https://www.rfc-editor.org/rfc/rfc-ref.txt'
RFC_URL = 'https://www.rfc-editor.org/rfc/'
RFC_LOCAL_REF = './rfc-ref.txt'
# this is the location where the RFC's will be downloaded
RFC_LOCATION = "./RFC/"

# @class Rfc
# @details class to contain the name of the RFC, the nuber of the same and the
# title of the RFC
class Rfc:
	def __init__(self, rfc_name, rfc_num, rfc_title):
		self.name = rfc_name
		self.num = rfc_num
		self.title = rfc_title
		self.url = RFC_URL

	def __init__(self):
		self.name = ''
		self.num = ''
		self.title = ''
		self.url = RFC_URL

	# set variable functions
	def set_name(self, rfc_name):
		self.name = rfc_name
	def set_num(self, rfc_num):
		self.num = rfc_num
	def set_title(self, rfc_title):
		self.title = rfc_title
	def set_url(self, rfc_url):
		self.url += rfc_url + ".txt"

	# get data functions
	def get_name(self):
		return self.name
	def get_num(self):
		return self.num
	def get_title(self):
		return self.title
	def get_url(self):
		return self.url

# @function get_rfc
# @details function to download the text file from the specified location. the
# file that will be downloaded is actually the index file containing
# information about the RFCs that have come out
def get_rfc(url_dwnl, filepath):
	response = urlopen(url_dwnl)
	data = response.read()
	lines = str(data).split('\n')

	# always rewrite the file - since the data content should never be
	# appended
	f = open(filepath, 'w')
	for line in lines:
		f.write(line + '\n')
	f.close()

# @function parse_name
# @details function to parse the name of the RFC from the line provided and
# then return the same as the result. If not found, return None
def parse_name(plist = []):
	for i in xrange(0, len(plist)):
		if 'RFC' in plist[i] and str(plist[i]).find('RFC') == 0:
			return str(plist[i]).strip()

# @function parse_title
# @details function to parse the RFC title from the string provided and then
# return the same else the value will be None
def parse_title(item):
	item = item.strip()
	return str(item[item.find('"') + 1:item.rfind('"')])

# @function parse_rfc_num
# @details function to parse the name of the rfc from the input string. If not
# found, return None
def parse_num(item):
	return str(item[item.rfind('/') + 1 : len(item) - 1])

# @function parse_rfc_ref
# @details function to parse the contents of the file as mentioned as the value
# of RFC_LOCAL_REF. After parsing the data has to be put into a map or
# container of some kind
def parse_rfc_ref(filepath):
	# the key would be the name of the RFC and the value would be the
	# object
	rfc_dict = {}

	# experimental control
	count = 0
	for line in inp([filepath]):
		if 'RFC' in line:
			line = line.strip()

			# experimental control
			count += 1

			# create an instance of the Rfc class and then push in
			# the
			# details in a container - create the container before
			# this
			# loop
			rt = Rfc()
			parsed_list = line.split('|')

			# get the name of the RFC
			rt.set_name(parse_name(parsed_list))

			# get the title of the RFC - sending in the last item
			rt.set_title(parse_title(parsed_list[len(parsed_list) -
				1]))

			# get the number of the RFC, set the url as well
			item = (parsed_list[len(parsed_list) - 1].strip())
			rt.set_num(parse_num(item.split(',')[-1].
				strip().strip('.')))
			rt.set_url(parse_num(item.split(',')[-1].
				strip().strip('.')))

			# putting another check for the non parsing of values
			#if rt.get_name() == 'RFC8262':
				#print(rt.get_name() + " " +
						#rt.get_title() + " " +
						#rt.get_num() + " " +
						#rt.get_url())

			# check if the name of the rfc is present in the
			# dictionary or not - if not push it in, if yes, forget
			# it
			if rt.get_name() not in rfc_dict:
				#print(rt.get_name())
				rfc_dict[rt.get_name()] = rt
			else:
				rt.get_name()

			if count == 8262:
				break

	# get the length of the dictionary
	#print(len(rfc_dict))
	#print(rfc_dict.get('RFC1248').get_title())
	return rfc_dict

# @function main
# @details function that performs the choreographing and calls the necessary
# functions based on the requirements
def main():
	# get the reference file downloaded
	print('Getting the index file from the internet')
	get_rfc(RFC_REF, RFC_LOCAL_REF)

	# now call the function which will be reading through the file
	print('\nParsing the information from the local file')
	rfc_dict = parse_rfc_ref(RFC_LOCAL_REF)

	# first check if the RFC directory has been created or not
	# if it is not created, create the directory
	if not path.isdir(RFC_LOCATION):
		# create the directory
		try:
			makedirs(RFC_LOCATION)
		except:
			pass

	while True:
		rfcstr = "RFC" + raw_input("RFC : ")
		if rfcstr == "RFCq" or rfcstr == 'RFCQ':
			break
		elif rfcstr == 'RFCl' or rfcstr == 'RFCL':
			# basically this will print all the RFCs already
			# present in the system and downloaded
			fl = glob(RFC_LOCATION + "/*.*")
			for i in fl:
				print(i)
		elif rfcstr in rfc_dict:
			print(rfc_dict[rfcstr].get_name() + " : " +
					rfc_dict[rfcstr].get_title())
			# if the RFC is found, get the file and then display it
			# using the editors available
			if not path.isfile(rfc_dict[rfcstr].get_name() +
					".txt"):
				get_rfc(rfc_dict[rfcstr].get_url(),
						RFC_LOCATION + "/" +
						rfc_dict[rfcstr].get_name() +
						".txt")
				system("nano " + RFC_LOCATION + "/" +
						rfc_dict[rfcstr].get_name() +
						".txt")
				system("clear")
		else:
			print(rfcstr + " doesn't exist, kindly check the RFC" +
					"num")

if __name__ == '__main__':
	main()
