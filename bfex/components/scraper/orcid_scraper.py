from bfex.components.scraper.scraper import *

class OrcIdScraper(Scraper):

    def get_scrapps(self):
        self.validate_url()
        soup = self.get_content()
        return []