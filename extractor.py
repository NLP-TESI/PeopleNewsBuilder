from knowledge import KnowledgeBase

class Extractor:

    def __init__(self, data=[]):
        self.data = data

    def extract(self): # will return a KnowledgeBase instance
        return KnowledgeBase()
