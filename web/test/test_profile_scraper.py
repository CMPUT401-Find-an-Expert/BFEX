import pytest
from bfex.components.scraper.profile_scraper import ProfileScraper
from bfex.components.scraper.scraper_type import ScraperType

base_url = "https://www.ualberta.ca/science/about-us/contact-us/faculty-directory/"


class TestProfileScraper():
    def test_create__success(self):
        my_scraper = ProfileScraper(base_url + "william-allison", ScraperType.PROFILE)
        assert my_scraper is not None
        assert my_scraper.url == base_url + "william-allison"
        assert my_scraper.type == ScraperType.PROFILE

        my_scraper.validate_url()

        soup = my_scraper.get_content()
        assert soup is not None

        scrapps = my_scraper.get_scrapps()
        assert scrapps is not None
        assert scrapps[0] is not None
        assert scrapps[0].meta_data is not None
        assert scrapps[0].meta_data["orcid_link"] is not None
        assert scrapps[0].meta_data["researchid_link"] is not None
