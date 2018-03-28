from flask import Blueprint, abort, render_template, make_response, request
from flask_restful import Resource, Api

from bfex.components.search_engine import parser, builder
from bfex.models import Faculty, Keywords
from bfex.common.schema import FacultySchema
from elasticsearch_dsl.search import Q

# Setup the blueprint and add to the api.
search_bp = Blueprint("search_api", __name__)
api = Api(search_bp)


class SearchAPI(Resource):
    """Contains methods for performing search over keywords."""

    def get(self):
        """HTTP Get that enables boolean query processing and search."""
        query = request.args.get('query')
        dept = request.args.get('dept')

        if query is None:
            abort(400)

        q_parser = parser.QueryParser()
        q_builder = builder.QueryBuilder()

        pf_query = q_parser.parse_query(query)
        elastic_query = q_builder.build(pf_query)
        response = Keywords.search().query(elastic_query)
        faculty_with_keywords = set(keywords.faculty_id for keywords in response.scan())

        if dept:
            should = [Q('prefix', department=k) for k in dept.split()]
            faculty = Faculty.search().query(Q('bool', should=should))
            dept_faculty = set(f.faculty_id for f in faculty.scan())
            faculty_with_keywords.intersection_update(dept_faculty)

        schema = FacultySchema()
        results = [schema.dump(Faculty.safe_get(faculty_id)) for faculty_id in faculty_with_keywords]
        return {
            "data": results
        }


api.add_resource(SearchAPI, '/search')
