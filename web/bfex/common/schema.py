from marshmallow import Schema, fields, post_load

from bfex.models import *


class FacultySchema(Schema):
    """Marshmallow schema used for validating Faculty JSON objects.

    A marshmallow schema allows us to easily extract information from JSON input, while at the same time, performing
    basic validation of that data.
    """
    faculty_id = fields.Integer(load_from="id", required=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)
    department = fields.String(allow_none=True, missing="Unknown")

    google_scholar = fields.String(load_from="googleScholarId")
    orc_id = fields.String(load_from="orcId")
    sciverse_id = fields.String(load_from="sciverseId")

    @post_load
    def _create_faculty(self, data):
        """Turns the extracted json data into an instance of Faculty"""
        return Faculty(meta={'id': data["faculty_id"]}, **data)
