import os

# NamedEntity class save a list of terms that represents one entity
# Each NamedEntity instance had a unique ID
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

# NamedEntitiesDict is used to load a dictionary of entities from a CSV file
class NamedEntitiesDict:
	# Load the entities dictionary from a file. All the entities are loaded here.
	# Two entities A and B can point to save NamedEntity instance. This means that the
	# entity with ID A and B are the same thing.
	@staticmethod
	def load_entities_dict_from_file(path, filename):
		f = open(os.path.join(path, filename), 'r')
		lines = f.read().split('\n')

		entities_dict = {}

		for line in lines:
			values = line.split(';')
			idt = int(values[0])
			ftr = int(values[1])
			terms = values[2:]

			entity = NamedEntity()
			entity.set_id(idt)
			entity.set_terms(terms)
			
			if(ftr not in entities_dict):
				entities_dict[ftr] = entity
				entities_dict[idt] = entity
			else:
				entities_dict[idt] = entities_dict[ftr]

		return entities_dict

	# Get only the entity father from the dictionary.
	@staticmethod
	def get_entities_fathers_dictionary(dct):
		lst = {}
		for key in dct:
			entity = dct[key]
			lst[entity.id()] = entity.terms()
		return lst