#https://github.com/elastic/elasticsearch-py/blob/64202273e02ab5f0b99271771d4e8143b3599c3e/elasticsearch/client/__init__.py
from elasticsearch import Elasticsearch
es = Elasticsearch()
body = {
    "doc": {
        "text_entry": "When wealthy industrialist Tony Stark is forced to build an armored suit after a life-threatening incident, he ultimately decides to use its technology to fight against evil."
    },
    "term_statistics": True,
    "field_statistics": True,
    "positions": False,
    "offsets": False,
    "filter": {
        "max_num_terms": 3,
        "min_term_freq": 1,
        "min_doc_freq": 1
    }
}
res = es.termvectors(index="shakespeare", doc_type="doc", body=body)
print(res)