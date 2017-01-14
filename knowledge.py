

class KnowledgeBase:

    def __init__(self, entities=None, relationships=None):
        self.entities = entities
        self.relationships = relationships

    def __getitem__(self, index):
        if index == "entities":
            return self.entities
        elif index == "relationships":
            return self.relationships
        else:
            raise IndexError

    def save(self, filename): # save csv of all data extracted
        self.save_entities("entities_"+filename)
        self.save_relationships("relationships_"+filename)

    def save_entities(self, filename):
        pass

    def save_relationships(self, filename):
        pass
