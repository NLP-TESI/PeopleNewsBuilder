#coding: utf-8
from knowledge import KnowledgeBase
from NamedEntity import NamedEntity
import TESIUtil
from Aelius import Extras, Toqueniza, AnotaCorpus
import nltk

class Extractor:

	ENTITIES_STOP_WORDS = {u'março',u'abstenção'}

	def __init__(self, data=[]):
		self.data = data
		self.HUNPOS = Extras.carrega('AeliusHunPos')


	def extract(self): # will return a KnowledgeBase instance
		global_entities = {}
		tagged_sentences = []

		for n in self.data:
			if n.text is None:
				continue
			sentences = Toqueniza.PUNKT.tokenize(n.text)
			tokenized = [Toqueniza.TOK_PORT.tokenize(sentence) for sentence in sentences]
			anoted = AnotaCorpus.anota_sentencas(tokenized, self.HUNPOS, 'hunpos')
			global_entities, taggeds = self._extract_entities(anoted, global_entities)
			tagged_sentences.append(taggeds)
			print taggeds

		distinct = TESIUtil.dict_to_list(global_entities)
		for i in distinct:
			print str(i.id()) + str(i)

		print(len(distinct))
		relationships = self._find_relationships(tagged_sentences)
		print relationships
		return KnowledgeBase(entities=global_entities, relationships=relationships)

	def _get_composed_verbs(self, sentence, start, end):
		composed_verb = sentence[start][0]
		aux = ""
		if('VB' in sentence[start][1]):
			for index in range(start-1,end-1,-1):
				if(index < 0 or start-index > 4):
					break
				item = sentence[index]
				aux = item[0] + " " + aux
				if("VB" in item[1]):
					composed_verb = aux + composed_verb
					break
		return composed_verb

	def _find_relationships(self, list_tagged):
		relationships = []

		for tagged in list_tagged:
			for index_sentence, sentence in enumerate(tagged):
				last_entity = None
				last_entity_index = 0
				last_relation = None

				percent = (index_sentence+1)/len(tagged)*100
				#print "\r"+str(round(percent, 1)) + "% ("+ str(index_sentence+1) +" de " + str(len(tagged)) + ")",

				for index, item in enumerate(sentence):
					if( len(item[0]) == 1 ):
						continue
					if('VB' in item[1]):
						last_relation = self._get_composed_verbs(sentence, index, last_entity_index)
					# elif( index < len(sentence)-1 and 'IN' == item[1] and 'DT' == sentence[index+1][1]):
					# 	last_relation = item[0] + " " + sentence[index+1][0]
					elif( len(item) == 3):
						if(last_entity is not None):
							if(index-last_entity_index == 2 and len(sentence[index-1][0])>1 ):
								relation = (sentence[index-1][0], last_entity[2], last_entity[0], item[2], item[0])
								relationships.append(relation)
								#print(relation)
							elif(last_relation is not None):
								relation = (last_relation, last_entity[2], last_entity[0], item[2], item[0])
								relationships.append(relation)
								#print(relation)
						last_entity = item
						last_entity_index = index
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

			for key in entities:
				if(key not in local_entities):
					local_entities[key] = entities[key]

			for k, item in enumerate(tagged_result):
				if(tagged_result[k][1] == 'NPR'):
					key = tagged_result[k][0]
					tagged_result[k] = (key, 'NPR', local_entities[key].id())

			taggeds.append(tagged_result)

		global_entities = self._find_similar_entities(global_entities, local_entities)

		return (global_entities, taggeds)

	def _find_similar_entities(self, global_entities, local_entities):
		final_dict = global_entities

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
				if(avg > 0.5 and avg > max_avg):
					best = item2


			if(best == None):
				final_dict[item1.id()] = item1
			else:
				final_dict[item1.id()] = best
				best.add_entity(item1)

		return final_dict

	def _analyze_sentence(self, anoted_sentence):
		entities = {}
		tagged = []
		i = 0

		while i < len(anoted_sentence):
			if(anoted_sentence[i][1] == 'NPR'):
				text = anoted_sentence[i][0]

				while(i+1 < len(anoted_sentence) and anoted_sentence[i+1][1] == 'NPR'):
					text += ' ' + anoted_sentence[i+1][0]
					i += 1

				if(text not in Extractor.ENTITIES_STOP_WORDS):
					if(text not in entities):
						e = NamedEntity(text)
						entities[text] = e
					else:
						e = entities[text]

					item = (text, 'NPR', e.id())
				else:
					item = (text, 'SYM')
			else:
				item = (anoted_sentence[i][0], anoted_sentence[i][1])

			tagged.append(item)
			i += 1

		return (entities, tagged)
