#coding: utf-8
import os
import TESIUtil

class KnowledgeBase:

	def __init__(self, entities_dict=None, taggeds=None, relations=None):
		self._entities = entities_dict
		self._relations = relations
		self._taggeds = taggeds

		if(not os.path.exists(os.path.join(u'knowledge_base'))):
			os.makedirs(os.path.join(u'knowledge_base'))

	def save(self, path_name): # save csv of all data extracted
		if(not os.path.exists(os.path.join(u'knowledge_base', path_name))):
			os.makedirs(os.path.join(u'knowledge_base', path_name))

		self._save_found_entities(path_name)

	def _save_found_entities(self, path_name):
		lines = []

		for key in self._entities:
			item = self._entities[key]
			tpl = []
			tpl.append(str(key))
			tpl.append(str(item.id()))
			tpl.append(';'.join(item.terms()))
			lines.append( ';'.join(tpl) )
		string = '\n'.join(lines)
		TESIUtil.save_file(os.path.join(u'knowledge_base',path_name), u"entities.csv", string.encode('UTF-8'))