import pytest
import requests
from bfex.components.scraper.scraper import Scraper
from bfex.components.scraper.scraper_type import ScraperType
from bfex.common.exceptions import ScraperException

base_url = "https://www.ualberta.ca/science/about-us/contact-us/faculty-directory/"


class TestScraper():
    def test_create__success(self):
        my_scraper = Scraper(base_url + "william-allison", ScraperType.PROFILE)
        assert my_scraper is not None
        assert my_scraper.url == base_url + "william-allison"
        assert my_scraper.type == ScraperType.PROFILE

        my_scraper.validate_url()
        
        soup = my_scraper.get_content()
        assert soup is not None
        
        scrapps = my_scraper.get_scrapps()
        assert scrapps == []

    def test_get_invalid_url__fail(self):
        my_scraper = Scraper("http://www.assdfghhded.com", ScraperType.PROFILE)
        with pytest.raises(requests.exceptions.ConnectionError):
            my_scraper.get_content()

    def test_validate__success(self):
        scraper = Scraper(base_url + "william-allison", ScraperType.PROFILE)
        scraper.validate_url()

        scraper = Scraper("http://researcherid.com/12345", ScraperType.RESEARCHID)
        scraper.validate_url()

        scraper = Scraper("http://scholar.google.ca/12345", ScraperType.GOOGLESCHOLAR)
        scraper.validate_url()

        scraper = Scraper("http://orcid.org/12345", ScraperType.ORCID)
        scraper.validate_url()

    def test_validate__fail(self):
        scraper = Scraper("https://w.bad-ualberta.ca/1234", ScraperType.PROFILE)
        with pytest.raises(ScraperException):
            scraper.validate_url()

        scraper = Scraper("http://researchid4.com/12345", ScraperType.RESEARCHID)
        with pytest.raises(ScraperException):
            scraper.validate_url()

        scraper = Scraper("http://scholar.not-good.google.ca/12345", ScraperType.GOOGLESCHOLAR)
        with pytest.raises(ScraperException):
            scraper.validate_url()

        scraper = Scraper("http://orcid-mistakes.org/12345", ScraperType.ORCID)
        with pytest.raises(ScraperException):
            scraper.validate_url()
