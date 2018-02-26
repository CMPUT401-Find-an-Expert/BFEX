from bfex.components.scraper.scraper import *

class ResearchIdScraper(Scraper):
    """ This is what will scrape the researchid links """

    def get_scrapps(self):
        """ Get the html content from the website and put it into a scrapp
            :return: return all the scrapps produced
        """
        self.validate_url()
        soup = self.get_content()
        return []
