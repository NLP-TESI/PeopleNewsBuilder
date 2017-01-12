import os

class NamedEntity:
	ID = 0

	def __init__(self, name=None):
		self._terms = {}
		if(name is not None):
			self._terms[name] = True
			self._id = NamedEntity.ID
			NamedEntity.ID += 1

	def terms(self):
		return self._terms

	def add_name(self, name):
		self._terms[name] = True

	def id(self):
		return self._id

	def set_id(self, i):
		self._id = i
		if(i > NamedEntity.ID):
			NamedEntity.ID = i+1

	def change_id(self, i):
		self._id = i

	def set_terms(self, lst):
		self._terms = lst

	def add_entity(self, item):
		for term in item.terms():
			self._terms[term] = True

	def __str__(self):
		return str(self._terms)