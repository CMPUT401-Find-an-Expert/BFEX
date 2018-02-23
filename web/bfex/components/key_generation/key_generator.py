
class KeyGenerator:
    def __init__(self):
        self.approaches = {}

    def generate_keywords(self, scrapp):
        result = {}
        for id in self.approaches.keys():
            result[id] = self.approaches[id](scrapp)
        return result

    def register_approach(self, callback, approachId):
        self.approaches[approachId] = callback

    def deregister_approach(self, approachId):
        del self.approaches[approachId]