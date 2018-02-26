import pytest
from bfex.models import *
from bfex.components.key_generation.key_generator import *
from bfex.components.key_generation.generic_approach import *
from bfex.components.scraper.scrapp import *

class TestKeyGenerator(object):
    def test_create_success(self):
        type_of_approach = 1
        my_key_generator = KeyGenerator()
        scrapp = Scrapp()
        scrapp.text = "The scraper is responsible from gathering useful information from our webpage data sources. It's goal is to extract any useful text, a title, dates and other meta-data (such as easily identifiable key words)from the page. It will then return that as a 'Scrapp'. A scrapp is a container for the results of a single page scraping"
        
        my_generic_approach = GenericApproach()
        my_key_generator.register_approach(my_generic_approach, type_of_approach)
        result = my_key_generator.generate_keywords(scrapp.text)
        assert result is not None

        my_key_generator.deregister_approach(type_of_approach)
        assert my_key_generator.approaches == {}
