
class KeyGenerator:
    """ 
    Each approach will be registered with the KeywordGenerator, which will iterate over all the registered approaches when generating keywords. It returns a structure of <approach_id, Array<keywords: String>> pairs which will let the user know which keywords generated each keyword.
    """
    def __init__(self):
        """
        :approaches Map of all approaches and their results
        """
        self.approaches = {}

    def generate_keywords(self, scrapp):
        """ Iterates through each registered approach and returns their result"""
        result = {}
        for id in self.approaches.keys():
            result[id] = self.approaches[id].generate_keywords(scrapp)
        return result

    def register_approach(self, obj, approachId):
        """ Register approach obj """
        self.approaches[approachId] = obj

    def deregister_approach(self, approachId):
        """ Removes approach obj """
        del self.approaches[approachId]