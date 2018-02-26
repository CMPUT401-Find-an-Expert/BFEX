from enum import Enum

class ScraperType(Enum):
        """ Enum class to keep track of all the different types of web pages 
            we can scrape.
        """
    ORCID = 1
    RESEARCHID = 2
    PROFILE = 3
