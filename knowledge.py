#coding: utf-8
import os
import TESIUtil

# This is to handle and save all knowledge collected
# This class is used to save the result of entire proccess
class KnowledgeBase:

	def __init__(self, entities_dict=None, taggeds=None, relations=None):
		self._entities = entities_dict
		self._relations = relations
		self._taggeds = taggeds
		self._base_folder = u"knowledge_base"

		if(not os.path.exists(os.path.join(self._base_folder))):
			os.makedirs(os.path.join(self._base_folder))

	# save csv of all data extracted
	def save(self, path_name):
		if(not os.path.exists(os.path.join(self._base_folder, path_name))):
			os.makedirs(os.path.join(self._base_folder, path_name))
		path_name = os.path.join(self._base_folder,path_name)

		self._save_found_entities(path_name)
		self._save_found_relationships(path_name)

	# save csv of all relations found
	def _save_found_relationships(self, path_name):
		header = "id;relation;entity1;id1;entity2;id2\n"
		with open(os.path.join(path_name,"relations.csv"),"w+") as out:
			out.write(header.encode('UTF-8'))
			for i,relation in enumerate(self._relations):
				line = unicode(i)
				for item in relation:
					line += ";"+unicode(item)
				line += u"\n"
				out.write(line.encode('UTF-8'))
			out.close()

	# save csv of all entities found
	def _save_found_entities(self, path_name):
		lines = []

		for i,item in enumerate(self._entities):
			tpl = []
			tpl.append(str(i))
			tpl.append(str(item.id()))
			tpl.append(','.join(item.terms()))
			lines.append( ';'.join(tpl) )
		string = '\n'.join(lines)
		TESIUtil.save_file(path_name, u"entities.csv", string.encode('UTF-8'))
