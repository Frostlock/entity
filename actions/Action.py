class Action(object):

    def process(self, text_blob):
        raise NotImplementedError("Subclass must implement abstract method: process(text_blob)")

    def log(self, msg):
        print(msg)
        return