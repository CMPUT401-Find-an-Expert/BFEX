from bfex.components.scraper.orcid_scraper import *
from bfex.components.scraper.researchid_scraper import *
from bfex.components.scraper.profile_scraper import *
from bfex.components.scraper.scraper_type import *


class ScraperFactory(object):
    """ Returns a scraper made for the URL you feed it """

    @staticmethod
    def create_scraper(url, type):
        """ Each type of website will need a different scraper to go through things
        
            :param url: url gotten from elastic search or other scrape.
            :param type: what type of webpage this is. This could be:
                - ResearcherID
                - OrcId
                - Profile page from faculty of science
                Each type will have similar web page design
            :return: a scraper made for that type of layout
        """
        if type == ScraperType.ORCID:
            return OrcIdScraper(url, type)
        if type == ScraperType.RESEARCHID:
            return ResearchIdScraper(url, type)
        if type == ScraperType.PROFILE:
            return ProfileScraper(url, type)