#coding: utf-8
import os
import shutil
import jellyfish
import distance
import re

HONOR_STOP_WORDS = [u'presidente', u'dona']

def create_or_replace_dir(dir_path):
	if (os.path.isdir(dir_path)):
		shutil.rmtree(dir_path)
	os.makedirs(dir_path)

def save_file(path, filename, text):
	text_file = open(build_dir_path(path, filename), 'w')
	text_file.write(text)
	text_file.close()

def build_dir_path(*paths):
	path = "."
	for p in paths:
		path += "/" + p
	return path

def index_of(lst, value):
	try:
		n = lst.index(value)
		return n
	except ValueError:
		return -1

def string_similarity(str1, str2):
	# str1 = str1.replace("'s", '').replace("ʼs", "")
	# str2 = str2.replace("'s", '').replace("ʼs", "")
	str1 = " ".join(re.findall("[a-zA-Z]+", str1))
	str2 = " ".join(re.findall("[a-zA-Z]+", str2))

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
		jaro = jellyfish.jaro_winkler(unicode(str1), unicode(str2))
	except TypeError:
		print "Error:",type(str1),type(str2)

	return cont*0.4 + jaro*0.6# + sw*0.1

def dict_to_list(dic):
	result_list = []
	for key in dic:
		if(dic[key] not in result_list):
			result_list.append(dic[key])
	return result_list

def remove_honor_words(string):
	result = ''
	temp = string.split(' ')

	for s in temp:
		if(s.lower() not in HONOR_STOP_WORDS):
			result += s + ' '

	return result.strip()
