from bfex.components.scraper.orcid_scraper import *
from bfex.components.scraper.researchid_scraper import *
from bfex.components.scraper.profile_scraper import *
from bfex.components.scraper.scraper_type import *


class ScraperFactory(object):

    @staticmethod
    def create_scraper(url, type):
        if type == ScraperType.ORCID:
            scraper = OrcIdScraper(url, type)
        if type == ScraperType.RESEARCHID:
            scraper = ResearchIdScraper(url, type)
        if type == ScraperType.PROFILE:
            print("thing")
            scraper = ProfileScraper(url, type)

        return scraper
