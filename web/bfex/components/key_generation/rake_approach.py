from bfex.components.key_generation.key_generation_approach import KeyGenerationApproach
from bfex.components.key_generation.RAKE import rake
import io


class RakeApproach(KeyGenerationApproach):
    def __init__(self):
        self.description = """ rake """
        self.apporach_id = 2
    
    def generate_keywords(self, scrapp):
        stop_words = "SmartStoplist.txt"
        
        rake_object  = rake.Rake(stop_words,5,3,4)

        text_file = io.open(scrapp, 'r')

        text = text_file.read

        keywords_with_score = rake_object.run(text)

        keywords = []

        for n in range(len(keywords_with_score)):
            keywords.append(keywords_with_score[n][0])

        return keywords

               
    def get_id(self):
        return self.approach_id

