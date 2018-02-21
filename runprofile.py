from bfex.components.scraper.scraper import *
from bfex.components.scraper.scraper_factory import *
from bfex.components.scraper.scraper_type import *
from bfex.common.utils import generate_names_from_json

import pickle

# this should be done with a real service but
# I do not know how that will work yet
data = json.load(open(r'../faculty.json'))
my_dict = {}
for item in data:
    formated_name = generate_names_from_json(item)
    # concatenate names into url
    url = base_url + formated_name

    scrapp = ScraperFactory.create_scraper(url, ScraperType.PROFILE)
    try:
        print(formated_name)
        print(scrapp[0].meta_data)
        mydict[formated_name] = scrapp[0]
    except:
        pass
pickle.dump( my_dict, open("dump.pkl", "wb"))