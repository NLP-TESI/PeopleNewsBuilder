import json

class News:
    def __init__(self, created=None, lastPublication=None, modified=None, publication=None,
                 id=None, summary=None, title=None, url=None, text=None):
        self.created = created
        self.lastPublication = lastPublication
        self.modified = modified
        self.publication = publication
        self.id = id
        self.summary = summary
        self.title = title
        self.url = url
        self.text = text

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

        self.created = data['created']
        self.lastPublication = data['lastPublication']
        self.modified = data['modified']
        self.publication = data['publication']
        self.id = data['id']
        self.summary = data['summary']
        self.title = data['title']
        self.url = data['url']
        self.text = data['text']