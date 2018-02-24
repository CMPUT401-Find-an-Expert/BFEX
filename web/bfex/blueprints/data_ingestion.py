from flask import Blueprint, abort, render_template, make_response, request
from flask_restful import Resource, Api

from bfex.models import *
from bfex.components.data_ingestor import DataIngester
from bfex.common.exceptions import DataIngestionException

MB = 1024 * 1024

# Setup the blueprint and add to the api.
data_ingestion_bp = Blueprint("data_ingestion", __name__)
api = Api(data_ingestion_bp)


class FacultyAPI(Resource):
    """Contains methods for performing basic CRUD operations on Faculty members"""

    def get(self, faculty_id):
        """ HTTP Get for the faculty resource.

        Currently returns an HTML page, but should instead return the Faculty object as JSON.

        :param faculty_id: The id as is in elasticsearch. This id is defined by the forum data dump.
        :return:HTTP 404 if the given ID does not exist.
                HTTP 200 if the id exists and the GET operation succeeds.
        """
        faculty = Faculty.safe_get(faculty_id)

        if faculty is None:
            abort(404)

        return make_response(render_template("faculty.html", faculty=faculty), 200, {'content-type': 'text/html'})


class FacultyListAPI(Resource):
    """Methods for performing some operations on lists of Faculty members."""

    def post(self):
        """HTTP Post for the faculty list resource.

        Ingests a lists of faculty members, and saves the information into elasticsearch. Currently does not do any
        checks if there already exists a faculty member with the same id that will be overridden.
        TODO: Decide if this should check for existing faculty and return which faculty were not inserted, and add PUT.

        :return:HTTP 400 if the request is not JSON.
                HTTP 413 if the given JSON is more than 16MB in size or there was an error ingesting the given data.
                HTTP 200 if the ingestion succeeded.
        """
        if not request.is_json:
            abort(400)

        # Data larger than 16MB should be broken up.
        if request.content_length > 16*MB:
            abort(413)

        json_data = request.get_json()

        try:
            DataIngester.bulk_create_faculty(json_data["data"])
        except DataIngestionException:
            abort(413)

        return 200


api.add_resource(FacultyAPI, '/faculty/<int:faculty_id>')
api.add_resource(FacultyListAPI, '/faculty')

