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
		kb = KnowledgeBase()
		global_entities = {}

		for n in self.data:
			sentences = Toqueniza.PUNKT.tokenize(n.text)
			tokenized = [Toqueniza.TOK_PORT.tokenize(sentence) for sentence in sentences]
			anoted = AnotaCorpus.anota_sentencas(tokenized, self.HUNPOS, 'hunpos')

			global_entities, taggeds = self._extract_entities(anoted, global_entities)

		
		distinct = TESIUtil.dict_to_list(global_entities)
		for i in distinct:
			print str(i.id()) + str(i)

		print(len(distinct))

		return kb

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

				if(term1 in item2.terms()):
					betters.append(item2)
				else:
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