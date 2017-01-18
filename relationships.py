
# This class is to manage the list of relations
# and keep no repetitive relationships 
class Relationships:

    def __init__(self):
        self.relations = {}

    # test if a relation already exist
    def _exist_relation(self, relation):
        relation_list = self.relations[relation[0].lower()]
        for r in relation_list:
            if r[0] == relation[1] and r[2] == relation[3]:
                return True
        return False

    # add a relation
    # relation = (relation_text, entity_id1, entity_text1, entitty_id2, entity_text2)
    def add(self, relation):
        if relation[0].lower() not in self.relations:
            self.relations[relation[0].lower()] = [relation[1:]]
        else:
            if not self._exist_relation(relation):
                self.relations[relation[0].lower()].append(relation[1:])

    def __len__(self):
        return sum(map(lambda x: len(x[1]), self.relations.items()))

    def __iter__(self):
        self.items = []
        for e in self.relations.items():
            for r in e[1]:
                self.items.append((e[0],r[0],r[1],r[2],r[3]))
        self.items.sort(key=lambda x: x[0])
        self.i = -1
        return self

    def next(self):
        if self.i >= len(self.items)-1:
            del self.items
            raise StopIteration
        else:
            self.i += 1
            return self.items[self.i]

    def __next__(self):
        return self.next()
