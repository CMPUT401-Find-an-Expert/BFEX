import pytest
from bfex.models import *
from bfex.components.key_generation.generic_approach import *
from bfex.components.key_generation.key_generator import *
from bfex.components.scraper.scrapp import *

class TestKeygen(object):
    def test_generic_approach(self):
        ga = GenericApproach(1,'generic')
        scrapp = Scrapp()
        scrapp.text = "The scraper is responsible from gathering useful information from our webpage data sources. It's goal is to extract any useful text, a title, dates and other meta-data (such as easily identifiable key words)from the page. It will then return that as a 'Scrapp'. A scrapp is a container for the results of a single page scraping"
        res = ga.generate_keywords(scrapp)
        print('generic',res)
        assert len(res) != 0
    def test_generator(self):
        kg = KeyGenerator()
        scrapp = Scrapp()
        scrapp.text = "The scraper is responsible from gathering useful information from our webpage data sources. It's goal is to extract any useful text, a title, dates and other meta-data (such as easily identifiable key words)from the page. It will then return that as a 'Scrapp'. A scrapp is a container for the results of a single page scraping"
        ga = GenericApproach(1,'test')
        kg.register_approach(ga,1)
        res = kg.generate_keywords(scrapp)
        print('generator',res)
        assert len(res) != 0