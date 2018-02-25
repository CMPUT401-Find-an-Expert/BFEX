from bfex.components.scraper.scraper import *
from bs4 import BeautifulSoup
from bfex.components.scraper.scrapp import *

class ProfileScraper(Scraper):

    def get_scrapps(self):
        scrapps = []
        self.validate_url()
        soup = self.get_content()
        links = soup.find_all("a")
        scrapp = Scrapp()
        for link in links:
            try:
                if 'orcid' in link.attrs['href']:
                    scrapp.add_meta("orcid_link", link.attrs['href'])
                if "researcherid" in link.attrs['href']:
                    scrapp.add_meta("researchid_link", link.attrs['href'])
            except KeyError:
                # not all 'a' tags have the links we want
                continue
        scrapps.append(scrapp)
        print("here")
        print("scrapps", scrapps)
        return scrapps