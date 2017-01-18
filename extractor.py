#coding: utf-8
from __future__ import print_function
from knowledge import KnowledgeBase
from NamedEntity import NamedEntity
from relationships import Relationships
import TESIUtil
from Aelius import Extras, Toqueniza, AnotaCorpus
import nltk

# This class extract thw entities and relationships from the news texts
class Extractor:

	# List of tokens that aren't entities. The proccess classified these as entity, but they aren't
	NOT_AN_ENTITY = { u'janeiro',u'fevereiro',u'março',u'abril',u'maio',u'junho',
					  u'julho',u'agosto',u'setembro',u'outubro',u'novembro',u'dezembro',
					  u'abstenção',u'r$',u'cenário',u'são',u'feira',u'segunda',u'terça',
					  u'quarta',u'quinta',u'sexta',u'sábado',u'domingo',u'tô', u'm', u'm.',
					  u'sócia', u'h.', u'us$', u'tampão', u'discurso'}

	def __init__(self, data=[], main_entity=None):
		self.data = data
		if main_entity is not None:
			self.main_entity = main_entity.lower()
		else:
			self.main_entity = None
		self.HUNPOS = Extras.carrega('AeliusHunPos')

	# Extract entities and relationships about the main entity
	def extract(self): # will return a KnowledgeBase instance
		# global_entities contains the entities extraction proccess result
		global_entities = {}
		# taggeds is used in relations extraction proccess
		taggeds = []

		# init the loop to extract entities
		for i,n in enumerate(self.data):
			if n.text is None:
				continue
			print('\rnews ' + str(i+1) + ' of ' + str(len(self.data)), end="")

			# tokenize the text by sentences
			sentences = Toqueniza.PUNKT.tokenize(n.text)
			# tokenize by words for each sentence. This is required to use anota_sentencas function
			tokenized = [Toqueniza.TOK_PORT.tokenize(sentence) for sentence in sentences]
			# Use the Aellius POSTagger to classify the tokens for each sentence.
			anoted = AnotaCorpus.anota_sentencas(tokenized, self.HUNPOS, 'hunpos')

			# Extract entities from the anoted text
			global_entities, tagged = self._extract_entities(anoted, global_entities)
			taggeds.append(tagged)

		# the the distinct list of entities extracted
		distinct = TESIUtil.dict_to_list(global_entities)

		# extract the relationships from tagged result
		relationships = self._find_relationships(taggeds, global_entities)

		total = sum(map(lambda x: len(x.terms()), distinct))

		print('\nentities distinct: ' + str(len(distinct)))
		print('total entities: ' + str(total))
		print('relationships: ' + str(len(relationships)))
		return KnowledgeBase(entities_dict=distinct, taggeds=taggeds, relations=relationships)

	# Identify the father entity.
	def _search_parent_entity(self, id, global_entities):
		aux = global_entities[id]
		while aux != global_entities[aux.id()]:
			aux = global_entities[aux.id()]
		return aux


	# Auxiliate in composition of relationships
	def _search_verb(self, sentence, start, end, relation_stops_type):
		final_verb = None
		for index in range(start-1,end-1,-1):
			if(index < 0 or start-index > 4):
				break
			item = sentence[index]
			if(item[1] in relation_stops_type):
				break
			if("VB" in item[1]):
				final_verb = item[0]
				break
		return final_verb

	# In order to buil a relation with one or more verbs
	def _get_composed_verbs(self, sentence, start, end, relation_stops_type):
		composed_verb = sentence[start][0]
		if('VB' in sentence[start][1]):
			final_verb = self._search_verb(sentence, start, end, relation_stops_type)
			if final_verb is not None:
				return final_verb+" "+composed_verb
		return composed_verb

	# In order to buil a relation with verb and noun
	def _compose_verb_noun(self, sentence, start, end, relation_stops_type):
		noun_type = ['N', 'N-P']
		if( sentence[start][1] in noun_type ):
			verb = self._search_verb(sentence, start, end, relation_stops_type)
			if verb is not None:
				return verb+" "+sentence[start][0]
		return None

	# In order to test if the main entity is one of thoses two entities
	def _contain_main_entity(self, entity1, entity2):
		if self.main_entity in entity1.lower() or self.main_entity in entity2.lower():
			return True
		else:
			return False

	# this function use the approaches to get the relations
	def _find_relationships(self, list_tagged, global_entities):
		relationships = Relationships()
		relation_stops_type = ['CONJ', 'WPRO', ',', '(', ')']
		relationship_stop_words = ['ex']

		for tagged in list_tagged:
			for index_sentence, sentence in enumerate(tagged):
				last_entity = None
				last_entity_index = 0
				last_relation = None

				for index, item in enumerate(sentence):
					# In order to avoid stop words
					if( len(item[0]) == 1 or item[0].lower() in relationship_stop_words):
						continue
					# to get the entity already identified
					elif( item[1] == 'NE'):
						# In order to build the relationship
						if(last_entity is not None and self._contain_main_entity(last_entity[0], item[0])):
							# to build a relationship with anything between entities
							# just if there is only one token between entities
							if(index-last_entity_index == 2 and len(sentence[index-1][0])>1 ):
								id1 = self._search_parent_entity(last_entity[2], global_entities).id()
								id2 = self._search_parent_entity(item[2], global_entities).id()
								relation = (sentence[index-1][0], id1, last_entity[0], id2, item[0])
								relationships.add(relation)
							# In order to build a relationship from relation already identified
							elif(last_relation is not None):
								id1 = self._search_parent_entity(last_entity[2], global_entities).id()
								id2 = self._search_parent_entity(item[2], global_entities).id()
								relation = (last_relation, id1, last_entity[0], id2, item[0])
								relationships.add(relation)
						last_entity = item
						last_entity_index = index
						last_relation = None

					# In order to get just relationships between entities
					if(last_entity is None):
						continue
					# In order to get relationship composed by verb and noun
					elif('N' in item[1]):
						last_relation = self._compose_verb_noun(sentence, index, last_entity_index, relation_stops_type)
					# In order to get relationship composed by one or more verbs
					elif('VB' in item[1]):
						last_relation = self._get_composed_verbs(sentence, index, last_entity_index, relation_stops_type)
					# In order to break relationships
					elif(item[1] in relation_stops_type):
						last_relation = None
						last_entity = None
						last_entity_index = 0

					# In order to remove relationships if a conjuction is found
					if last_relation is not None and last_relation[0].isupper():
						last_relation = None

		return relationships

	def _extract_entities(self, anoted, global_entities):
		local_entities = {}
		taggeds = []
		# special cases to extract entities
		for anoted_sentence in anoted:
			for i, word in enumerate(anoted_sentence):
				if(i+1 < len(anoted_sentence) and word[0] == 'Lava' and anoted_sentence[i+1][0] == 'Jato'):
					anoted_sentence[i] = (word[0], 'NPR')
				elif(i+1 < len(anoted_sentence) and word[0].lower() in ['da', 'do'] and anoted_sentence[i+1][0].lower() in ['silva', 'campo', 'jaburu']):
					anoted_sentence[i] = (word[0], 'NPR')

		# identifying entities
		for anoted_sentence in anoted:
			entities, tagged_result = self._analyze_sentence(anoted_sentence)

			# In order to avoid equals local entities (same text token)
			for key in entities:
				if(key not in local_entities):
					local_entities[key] = entities[key]

			# save in tagged_result as NE (Named Entity) with these ID
			for k, item in enumerate(tagged_result):
				if(tagged_result[k][1] == 'NE'):
					key = tagged_result[k][0]
					tagged_result[k] = (key, 'NE', local_entities[key].id())

			taggeds.append(tagged_result)

		# use the well known entities at global_entities to find correlations with local_entities founds
		# use string similarity to find similars entities.
		# if a local entity is in glogal entities, your instance is updated
		# else create a new entry at globals.
		global_entities = self._find_similar_entities(global_entities, local_entities)

		return (global_entities, taggeds)

	# Verify if entity already exists in global_entities
	# and try to merge entities like "Dilma" and "Dilma Rousseff"
	def _find_similar_entities(self, global_entities, local_entities):
		final_dict = global_entities

		# for each local entity, try to find globals candidates that can be similar
		for key1 in local_entities:
			item1 = local_entities[key1]

			term1 = list(item1.terms().keys())[0]
			str1 = TESIUtil.remove_honor_words(list(item1.terms().keys())[0])
			str1 = term1

			best = None
			max_avg = 0.0

			for key2 in final_dict:
				item2 = final_dict[key2]
				sum_sim = 0
				qty = 0

				for term2 in item2.terms():
					str2 = TESIUtil.remove_honor_words(term2)
					str2 = term2

					sum_sim += TESIUtil.string_similarity(str1, str2)
					qty += 1
				avg = sum_sim/qty
				# 0.7 is the min similarity to get as similar
				if(avg > 0.7 and avg > max_avg):
					best = item2
					max_avg =  avg

			if(best == None):
				final_dict[item1.id()] = item1
			else:
				final_dict[item1.id()] = best
				best.add_entity(item1)

		return final_dict

	# Analyze sentence to find named entities localy
	def _analyze_sentence(self, anoted_sentence):
		entities = {}
		tagged = []
		i = 0

		# Test if the sentence contains main entity("dilma").
		# If not, none proccess of extract entities is done to this sentence
		# Only sentences with the main entity will be relevant to extract these relations
		contains_main_entity = False
		for a in anoted_sentence:
			if(self.main_entity in a[0].lower()):
				contains_main_entity = True
				break

		if(contains_main_entity):
			while i < len(anoted_sentence):
				# Find a NPR token. NPR = nome proprio
				if(anoted_sentence[i][1] == 'NPR'):
					text = anoted_sentence[i][0]

					# Find sequences of NPR
					while(i+1 < len(anoted_sentence) and anoted_sentence[i+1][1] == 'NPR'):
						text += ' ' + anoted_sentence[i+1][0]
						i += 1

					# Test and add the found entity at result
					if(text.lower() not in Extractor.NOT_AN_ENTITY):
						if(text not in entities):
							e = NamedEntity(text)
							entities[text] = e
						else:
							e = entities[text]

						item = (text, 'NE', e.id())
					else:
						item = (text, 'SYM')
				else:
					item = (anoted_sentence[i][0], anoted_sentence[i][1])

				tagged.append(item)
				i += 1
		else:
			# if not contains main entity, does not extract entities in sentence
			for item in anoted_sentence:
				tagged.append(item)

		return (entities, tagged)
