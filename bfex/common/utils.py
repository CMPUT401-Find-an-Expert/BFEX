import re

def generate_names_from_json(item):
    name_from_json = item['name']
    name_from_json = re.sub('[.]', '', name_from_json)
    name_list = re.findall('[A-Z][^A-Z]*', name_from_json)
    formated_name = "-".join(name_list).lower()
    return formated_name
