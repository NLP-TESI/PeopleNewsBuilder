import json

class News:
    def __init__(self, **kwargs):
        self.load(**kwargs)

    def load(self, **data):
        self.created = data.get('created')
        self.lastPublication = data.get('lastPublication')
        self.modified = data.get('modified')
        self.publication = data.get('publication')
        self.id = data.get('id')
        self.summary = data.get('summary')
        self.title = data.get('title')
        self.url = data.get('url')
        self.text = data.get('text')

    def dumpsToJSON(self, path):
        j = { 'created': self.created, 'lastPublication': self.lastPublication,
              'modified': self.modified, 'publication': self.publication, 'id': self.id,
              'summary': self.summary, 'title': self.title, 'url': self.url, 'text': self.text }

        f = open(path, 'w')
        f.write(json.dumps(j))
        f.close()

    def loadsFromJSON(self, path):
        f = open(path, 'r')
        data = json.loads(f.read())
        self.load(**data)
