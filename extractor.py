from knowledge import KnowledgeBase

from Aelius import Extras, Toqueniza, AnotaCorpus
import nltk

class Extractor:

	def __init__(self, data=[]):
		self.data = data
		self.HUNPOS = Extras.carrega('AeliusHunPos')


	def extract(self): # will return a KnowledgeBase instance
		kb = KnowledgeBase()

		for n in self.data:
			sentences = Toqueniza.PUNKT.tokenize(n.text)
			tokenized = [Toqueniza.TOK_PORT.tokenize(sentence) for sentence in sentences]
			anoted = AnotaCorpus.anota_sentencas(tokenized, self.HUNPOS, 'hunpos')

		return kb
