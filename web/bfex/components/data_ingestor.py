from collections.abc import Sequence

from marshmallow.exceptions import ValidationError
from bfex.common.schema import *
from bfex.common.exceptions import DataIngestionException
from bfex.components.data_pipeline.tasks import GetFacultyFromElasticSearch, FacultyPageScrape, UpdateFacultyFromScrape
from bfex.tasks import run_workflow
from bfex.components.data_pipeline.workflow import Workflow

class DataIngester(object):
    INITIAL_PAGE_SCRAPE = [FacultyPageScrape, UpdateFacultyFromScrape]

    @staticmethod
    def create_faculty(json_data, write=True):
        """Creates an instance of Faculty from a JSON representation.

        :param dict json_data: Dictionary representation of the JSON data.
        :param bool write: Boolean switch that will enable writing to elastic.
        """
        schema = FacultySchema()

        try:
            faculty = schema.load(json_data)
        except ValidationError as err:
            raise DataIngestionException("Missing one of the required fields of the schema. {}"
                                         .format(err.messages))

        if write:
            faculty.save()

    @staticmethod
    def bulk_create_faculty(json_data, write=True):
        """Takes in a list of JSON objects, and loads them into elasticsearch.

        :exception TypeError: If the json_data is not a sequence object. The expected type is a List.
        """
        if not isinstance(json_data, Sequence):
            raise TypeError("Expected a Sequence, but got a {}", type(json_data))

        count = 0
        for faculty_member in json_data:
            count += 1
            DataIngester.create_faculty(faculty_member, write)

        search = Faculty.search()
        allFaculty = [faculty for faculty in search.scan()]
        for faculty in allFaculty:

            if isinstance(faculty, str):
                faculty_name = faculty
            else:
                faculty_name = faculty.name
            print(faculty)

            # TODO: This should be running in the create_faculty, once we fix the workflow.
            workflow = Workflow(DataIngester.INITIAL_PAGE_SCRAPE, faculty_name)
            run_workflow.apply_async((workflow,), countdown=5)
            print("Ingested {} faculty members".format(count))

    @staticmethod
    def create_grant(json_data, write=True):
        pass

    @staticmethod
    def bulk_create_grants(json_data, write=True):
        pass

    @staticmethod
    def create_publication(json_data, write=True):
        pass

    @staticmethod
    def bulk_create_publications(json_data, write=True):
        pass
