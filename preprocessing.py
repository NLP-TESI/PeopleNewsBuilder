from News import News

class PreProcessing:

    def __init__(self, files=[]):
        self.data = [ self.processing(f) for f in files ]

    def processing(self, file_new):
        n = News()
        n.loadsFromJSON(file_new)
        #do something with n.text
        if n.text is not None:
            n.text = n.text.replace("]"," ").strip()
            n.text = n.text.replace("["," ").strip()
        return n

    def __iter__(self):
        self.i = -1
        return self

    def __next__(self):
        if self.i >= len(self.data):
            del self.i
            raise StopIteration
        else:
            self.i += 1
            return self.data[self.i]
