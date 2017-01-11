#coding: utf-8
from knowledge import KnowledgeBase

from Aelius import Extras, Toqueniza, AnotaCorpus
import nltk

class Extractor:

	ENTITIES_STOP_WORDS = {u'março',u'abstenção'}

	def __init__(self, data=[]):
		self.data = data
		self.HUNPOS = Extras.carrega('AeliusHunPos')


	def extract(self): # will return a KnowledgeBase instance
		kb = KnowledgeBase()

		for n in self.data:
			sentences = Toqueniza.PUNKT.tokenize(n.text)
			tokenized = [Toqueniza.TOK_PORT.tokenize(sentence) for sentence in sentences]
			anoted = AnotaCorpus.anota_sentencas(tokenized, self.HUNPOS, 'hunpos')

			local_entities = self._extract_entities(anoted)
			print(local_entities)

		return kb

	def _extract_entities(self, anoted):
		local_entities = {}

		# special cases to extract entities
		for anoted_sentence in anoted:
			for i, word in enumerate(anoted_sentence):
				if(i+1 < len(anoted_sentence) and word[0] == 'Lava' and anoted_sentence[i+1][0] == 'Jato'):
					anoted_sentence[i] = (word[0], 'NPR')
				elif(i+1 < len(anoted_sentence) and word[0].lower() in ['da', 'do'] and anoted_sentence[i+1][0].lower() in ['silva', 'campo', 'jaburu']):
					anoted_sentence[i] = (word[0], 'NPR')

		# identifying entities
		for anoted_sentence in anoted:
			i = 0
			while i < len(anoted_sentence):
				if(anoted_sentence[i][1] == 'NPR'):
					text = anoted_sentence[i][0]

					while(i+1 < len(anoted_sentence) and anoted_sentence[i+1][1] == 'NPR'):
						text += ' ' + anoted_sentence[i+1][0]
						i += 1
					
					if(text not in Extractor.ENTITIES_STOP_WORDS):
						local_entities[text] = text # replace by a NamedEntity class
				i += 1
		return local_entities
