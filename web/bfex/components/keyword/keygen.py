# https://www.elastic.co/guide/en/elasticsearch/reference/6.2/docs-termvectors.html
from flask import Blueprint, abort, render_template, make_response, request
from flask_restful import Resource, Api
from bfex.models import *
from elasticsearch import Elasticsearch

MB = 1024 * 1024

# Setup the blueprint and add to the api.
keygen_bp = Blueprint("keygen", __name__)
api = Api(keygen_bp)
es = Elasticsearch()

class TfidfAPI(Resource):
    """Contains methods for pulling tfidf scores on keywords"""

    def get(self, query):
        """ HTTP Get for the keywords.

        Currently returns tfidf scores of all documents, but should instead return the professor & keywords as JSON
        """
        body = {
            "doc": {
                "text": query
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

        publication = es.termvectors(
            index="Publication", doc_type="doc", body=body)

        if publication is None:
            abort(404)

        return make_response(render_template("publication.html", publication=publication), 200, {'content-type': 'text/html'})

api.add_resource(TfidfAPI, '/keygen/<query>')
