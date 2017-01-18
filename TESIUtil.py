#coding: utf-8
import os
import shutil
import jellyfish
import distance
import re

# Words that should be removed befere the string similarity calc.
HONOR_STOP_WORDS = [u'presidente', u'dona']

# Create a dir or replace with empty dir if it already exists
def create_or_replace_dir(dir_path):
	if (os.path.isdir(dir_path)):
		shutil.rmtree(dir_path)
	os.makedirs(dir_path)

# save a text in a file
def save_file(path, filename, text):
	text_file = open(build_dir_path(path, filename), 'w')
	text_file.write(text)
	text_file.close()

# build a path to a directory.
# Deprecated: should use os.path.join instead this method
def build_dir_path(*paths):
	path = "."
	for p in paths:
		path += "/" + p
	return path

# Get first index of a value at list
def index_of(lst, value):
	try:
		n = lst.index(value)
		return n
	except ValueError:
		return -1

# Calculate the similarity between two strings
# Return a value between 0 and 1, where 0 is totaly differents and 1 is totaly equals
def string_similarity(str1, str2):
	# remove any character that isn't alphanumeric
	str1 = " ".join(re.findall("[a-zA-Z]+", str1))
	str2 = " ".join(re.findall("[a-zA-Z]+", str2))
	# if length of str1 or str2 is 0, return 0
	if(len(str1) == 0 or len(str2) == 0):
		return 0

	# This if/else is to define the Belonging Coeficient (cont)
	if(str1 in str2 or str2 in str1):
		temp1 = str1.split(' ')
		temp2 = str2.split(' ')
		if(temp1[len(temp1)-1] == temp2[len(temp2)-1] and (len(temp1) == 1 or len(temp2) == 1)):
			cont = 0.5
		else:
			cont = 1
	else:
		cont = 0
	try:
		# use jellyfish jaro winkler function
		jaro = jellyfish.jaro_winkler(unicode(str1), unicode(str2))
	except TypeError:
		print "Error:",type(str1),type(str2)

	# 0.4 and 0.6 was defined empirically
	return cont*0.4 + jaro*0.6

# return the distinct instances of a dictionary as a list
def dict_to_list(dic):
	result_list = []
	for key in dic:
		if(dic[key] not in result_list):
			result_list.append(dic[key])
	return result_list

# Use the HONOR_STOP_WORDS array to remove occurrences in a string
def remove_honor_words(string):
	result = ''
	temp = string.split(' ')

	for s in temp:
		if(s.lower() not in HONOR_STOP_WORDS):
			result += s + ' '

	return result.strip()
