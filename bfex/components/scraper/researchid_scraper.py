from bfex.components.scraper.scraper import *

class ResearchIdScraper(Scraper):

    def get_scrapps(self):
        self.validate_url()
        soup = self.get_content()
        return []
